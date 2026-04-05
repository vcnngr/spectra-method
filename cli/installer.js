/**
 * SPECTRA Installer -- Core installation logic
 *
 * Separated from CLI for testability and reuse.
 * Handles all file operations: detection, copy, backup, restore, manifest writing,
 * skill registration, output directory creation, and inline config writing.
 */

import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import YAML from 'yaml';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

/** Files/directories to skip during copy */
const COPY_EXCLUSIONS = [
  'node_modules',
  '_spectra-output',
  '.DS_Store',
  '.git',
  '.tmp',
  'package-lock.json',
  'package.json',  // NPM package config, not for end users
  'cli',           // Don't copy the CLI into the target -- it runs from npx
  'DEV-GUIDE.md',  // Development guide, not for end users
  'README.md',     // NPM readme, not for end users (SPECTRA.md is the reference)
  'LICENSE',        // Included in npm, not needed in installed project
  'CHANGELOG.md',  // Release history, not for end users
  '.npmignore',    // NPM packaging config
  'validate-spectra.py',  // Development validation tool
  'e2e-test-report.md',   // Test report
];

/** User config files that should be preserved across updates */
const USER_CONFIG_PATTERNS = [
  'config.yaml',
  'engagement.yaml',
];

/** Directories that represent installable modules */
const MODULE_DIRS = {
  core: 'core',
  rtk:  'rtk',
  soc:  'soc',
  irt:  'irt',
  grc:  'grc',
};

/** Top-level framework files to always copy */
const FRAMEWORK_FILES = [
  'SPECTRA.md',
];

/** Top-level framework directories to always copy */
const FRAMEWORK_DIRS = [
  '_config',
];

/** Default output subdirectories */
const OUTPUT_SUBDIRS = [
  'engagements',
  'reports',
  'evidence',
];

// ---------------------------------------------------------------------------
// Project Root Detection
// ---------------------------------------------------------------------------

/**
 * Detect the target project root directory.
 *
 * Resolution order:
 *   1. Explicit --directory / --target flag value
 *   2. Current working directory
 *
 * @param {string|undefined} explicitTarget - Path from --directory or --target flag
 * @returns {string} Absolute path to project root
 */
export function detectProjectRoot(explicitTarget) {
  if (explicitTarget) {
    const resolved = path.resolve(explicitTarget);
    if (!fs.existsSync(resolved)) {
      fs.mkdirSync(resolved, { recursive: true });
    }
    return resolved;
  }
  return process.cwd();
}

// ---------------------------------------------------------------------------
// Existing Installation Check
// ---------------------------------------------------------------------------

/**
 * Check if SPECTRA is already installed at the target path.
 *
 * @param {string} spectraDir - Path to _spectra/ directory
 * @returns {{ exists: boolean, version?: string, installDate?: string, hasConfig?: Object }}
 */
export function checkExistingInstallation(spectraDir) {
  const result = { exists: false, hasConfig: {} };

  if (!fs.existsSync(spectraDir)) {
    return result;
  }

  result.exists = true;

  // Try to read manifest
  const manifestPath = path.join(spectraDir, '_config', 'manifest.yaml');
  if (fs.existsSync(manifestPath)) {
    try {
      const content = fs.readFileSync(manifestPath, 'utf-8');
      const manifest = YAML.parse(content);
      result.version = manifest?.installation?.version;
      result.installDate = manifest?.installation?.installDate;
    } catch {
      // Manifest unreadable -- proceed anyway
    }
  }

  // Check which modules have config files
  for (const [modName, modDir] of Object.entries(MODULE_DIRS)) {
    const configPath = path.join(spectraDir, modDir, 'config.yaml');
    result.hasConfig[modName] = fs.existsSync(configPath);
  }

  return result;
}

// ---------------------------------------------------------------------------
// File Copy
// ---------------------------------------------------------------------------

/**
 * Copy SPECTRA framework files from source (npm package) to target project.
 *
 * @param {string} sourcePath - Path to the SPECTRA source (npm package root)
 * @param {string} targetPath - Path to target _spectra/ directory
 * @param {{ modules?: string[] }} options - Installation options
 * @returns {{ fileCount: number, dirCount: number }}
 */
export function copyFrameworkFiles(sourcePath, targetPath, options = {}) {
  const modules = options.modules || Object.keys(MODULE_DIRS);
  let fileCount = 0;
  let dirCount = 0;

  // Ensure target directory exists
  fs.mkdirSync(targetPath, { recursive: true });

  // Copy top-level framework files
  for (const file of FRAMEWORK_FILES) {
    const src = path.join(sourcePath, file);
    const dst = path.join(targetPath, file);
    if (fs.existsSync(src)) {
      fs.copyFileSync(src, dst);
      fileCount++;
    }
  }

  // Copy top-level framework directories
  for (const dir of FRAMEWORK_DIRS) {
    const src = path.join(sourcePath, dir);
    const dst = path.join(targetPath, dir);
    if (fs.existsSync(src)) {
      const result = copyDirRecursive(src, dst);
      fileCount += result.files;
      dirCount += result.dirs;
    }
  }

  // Copy each requested module
  for (const mod of modules) {
    const modDir = MODULE_DIRS[mod];
    if (!modDir) continue;

    const src = path.join(sourcePath, modDir);
    const dst = path.join(targetPath, modDir);

    if (fs.existsSync(src)) {
      const result = copyDirRecursive(src, dst);
      fileCount += result.files;
      dirCount += result.dirs;
    }
  }

  return { fileCount, dirCount };
}

/**
 * Recursively copy a directory, respecting exclusions.
 * Does NOT overwrite files matching USER_CONFIG_PATTERNS.
 *
 * @param {string} src - Source directory
 * @param {string} dst - Destination directory
 * @returns {{ files: number, dirs: number }}
 */
function copyDirRecursive(src, dst) {
  let files = 0;
  let dirs = 0;

  fs.mkdirSync(dst, { recursive: true });
  dirs++;

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcEntry = path.join(src, entry.name);
    const dstEntry = path.join(dst, entry.name);

    // Skip excluded files/directories
    if (COPY_EXCLUSIONS.includes(entry.name)) {
      continue;
    }

    if (entry.isDirectory()) {
      const result = copyDirRecursive(srcEntry, dstEntry);
      files += result.files;
      dirs += result.dirs;
    } else if (entry.isFile()) {
      // Don't overwrite user config files if they already exist
      const isUserConfig = USER_CONFIG_PATTERNS.includes(entry.name);
      if (isUserConfig && fs.existsSync(dstEntry)) {
        continue;
      }

      fs.copyFileSync(srcEntry, dstEntry);
      files++;
    }
  }

  return { files, dirs };
}

// ---------------------------------------------------------------------------
// User Config Preservation
// ---------------------------------------------------------------------------

/**
 * Backup user config files before an update.
 *
 * Walks the _spectra/ directory and saves the content of any file
 * matching USER_CONFIG_PATTERNS.
 *
 * @param {string} spectraDir - Path to _spectra/ directory
 * @returns {{ count: number, configs: Array<{ relativePath: string, content: string }> }}
 */
export function preserveUserConfigs(spectraDir) {
  const configs = [];

  function walk(dir, relativeBase) {
    if (!fs.existsSync(dir)) return;

    const entries = fs.readdirSync(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relativePath = path.join(relativeBase, entry.name);

      if (entry.isDirectory()) {
        if (!COPY_EXCLUSIONS.includes(entry.name)) {
          walk(fullPath, relativePath);
        }
      } else if (entry.isFile() && USER_CONFIG_PATTERNS.includes(entry.name)) {
        try {
          const content = fs.readFileSync(fullPath, 'utf-8');
          configs.push({ relativePath, content });
        } catch {
          // Skip unreadable files
        }
      }
    }
  }

  walk(spectraDir, '');
  return { count: configs.length, configs };
}

/**
 * Restore previously backed-up user config files.
 *
 * @param {string} spectraDir - Path to _spectra/ directory
 * @param {{ configs: Array<{ relativePath: string, content: string }> }} savedConfigs
 */
export function restoreUserConfigs(spectraDir, savedConfigs) {
  if (!savedConfigs || !savedConfigs.configs) return;

  for (const { relativePath, content } of savedConfigs.configs) {
    const fullPath = path.join(spectraDir, relativePath);
    const dir = path.dirname(fullPath);

    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(fullPath, content, 'utf-8');
  }
}

// ---------------------------------------------------------------------------
// Skill Registration for IDE
// ---------------------------------------------------------------------------

/**
 * Parse the skill-manifest.csv and return skill entries.
 *
 * @param {string} csvPath - Absolute path to skill-manifest.csv
 * @returns {Array<{ canonicalId: string, name: string, description: string, module: string, path: string, installToSpectra: boolean }>}
 */
function parseSkillManifest(csvPath) {
  if (!fs.existsSync(csvPath)) {
    return [];
  }

  const content = fs.readFileSync(csvPath, 'utf-8');
  const lines = content.trim().split('\n');

  if (lines.length < 2) return [];

  // Parse header
  const header = parseCSVLine(lines[0]);
  const idxId = header.indexOf('canonicalId');
  const idxName = header.indexOf('name');
  const idxDesc = header.indexOf('description');
  const idxModule = header.indexOf('module');
  const idxPath = header.indexOf('path');
  const idxInstall = header.indexOf('install_to_spectra');

  const skills = [];

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    const cols = parseCSVLine(line);
    skills.push({
      canonicalId: cols[idxId] || '',
      name: cols[idxName] || '',
      description: cols[idxDesc] || '',
      module: cols[idxModule] || '',
      path: cols[idxPath] || '',
      installToSpectra: (cols[idxInstall] || '').toLowerCase() === 'true',
    });
  }

  return skills;
}

/**
 * Parse a single CSV line, handling quoted fields.
 *
 * @param {string} line
 * @returns {string[]}
 */
function parseCSVLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && i + 1 < line.length && line[i + 1] === '"') {
        // Escaped quote
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === ',' && !inQuotes) {
      result.push(current);
      current = '';
    } else {
      current += ch;
    }
  }

  result.push(current);
  return result;
}

/**
 * Register SPECTRA skills for a specific IDE by creating symlinks
 * in the IDE's skill discovery directory.
 *
 * For Claude Code: creates symlinks in {projectRoot}/.claude/skills/{canonicalId}/
 * pointing to the actual skill directory in _spectra/.
 *
 * Symlinks preserve relative references (./workflow.md, ./steps-c/, ./scripts/)
 * that skills use internally.
 *
 * @param {string} projectRoot - Absolute path to the project root
 * @param {string} ide - IDE identifier (e.g., "claude-code")
 * @param {{ modules?: string[], spectraDir?: string }} options
 * @returns {{ registered: number, skipped: number, errors: string[] }}
 */
export function registerSkillsForIDE(projectRoot, ide, options = {}) {
  const spectraDir = options.spectraDir || path.join(projectRoot, '_spectra');
  const requestedModules = options.modules || Object.keys(MODULE_DIRS);
  const result = { registered: 0, skipped: 0, errors: [] };

  // Read skill manifest
  const csvPath = path.join(spectraDir, '_config', 'skill-manifest.csv');
  const skills = parseSkillManifest(csvPath);

  if (skills.length === 0) {
    result.errors.push('skill-manifest.csv not found or empty');
    return result;
  }

  // Filter to requested modules and installable skills
  const filteredSkills = skills.filter(s =>
    s.installToSpectra && requestedModules.includes(s.module)
  );

  // Determine target directory based on IDE
  let skillsTargetDir;
  if (ide === 'claude-code') {
    skillsTargetDir = path.join(projectRoot, '.claude', 'skills');
  } else if (ide === 'cursor') {
    // Future: Cursor uses a different path
    skillsTargetDir = path.join(projectRoot, '.cursor', 'skills');
  } else {
    result.errors.push(`Unsupported IDE: ${ide}`);
    return result;
  }

  // Ensure target directory exists
  fs.mkdirSync(skillsTargetDir, { recursive: true });

  for (const skill of filteredSkills) {
    const skillId = skill.canonicalId;

    // The path in the CSV is like "_spectra/core/spectra-init/SKILL.md"
    // We need the directory containing SKILL.md
    const skillRelativePath = skill.path;
    const skillDir = path.dirname(skillRelativePath); // e.g., "_spectra/core/spectra-init"

    // Source: the actual skill directory in the project (after framework files are copied)
    const sourceDir = path.join(projectRoot, skillDir);

    // Destination: the symlink in .claude/skills/
    const destLink = path.join(skillsTargetDir, skillId);

    if (!fs.existsSync(sourceDir)) {
      result.errors.push(`Source not found: ${sourceDir}`);
      result.skipped++;
      continue;
    }

    // Remove existing entry (file, dir, or symlink) before creating
    if (fs.existsSync(destLink) || isSymlinkBroken(destLink)) {
      try {
        const stat = fs.lstatSync(destLink);
        if (stat.isSymbolicLink() || stat.isFile()) {
          fs.unlinkSync(destLink);
        } else if (stat.isDirectory()) {
          fs.rmSync(destLink, { recursive: true });
        }
      } catch {
        // If lstat fails, try unlink anyway
        try { fs.unlinkSync(destLink); } catch { /* ignore */ }
      }
    }

    // Create symlink: try relative symlink first for portability
    try {
      const relativeSource = path.relative(skillsTargetDir, sourceDir);
      fs.symlinkSync(relativeSource, destLink, 'dir');
      result.registered++;
    } catch {
      // Symlink failed (e.g., Windows without admin) -- fall back to copy
      try {
        const copyResult = copyDirRecursive(sourceDir, destLink);
        result.registered++;
      } catch (copyErr) {
        result.errors.push(`Failed to register ${skillId}: ${copyErr.message}`);
        result.skipped++;
      }
    }
  }

  return result;
}

/**
 * Check if a path is a broken symlink.
 *
 * @param {string} p
 * @returns {boolean}
 */
function isSymlinkBroken(p) {
  try {
    fs.lstatSync(p);   // lstat doesn't follow symlinks
    fs.statSync(p);    // stat follows symlinks -- will throw if target is missing
    return false;
  } catch {
    try {
      fs.lstatSync(p); // If lstat succeeds but stat failed, it's a broken symlink
      return true;
    } catch {
      return false;     // Path doesn't exist at all
    }
  }
}

// ---------------------------------------------------------------------------
// Output Directory Creation
// ---------------------------------------------------------------------------

/**
 * Create the output directory for engagement artifacts.
 *
 * Creates the main output folder and standard subdirectories:
 * - engagements/  -- per-engagement working directories
 * - reports/      -- generated reports
 * - evidence/     -- evidence chain artifacts
 *
 * @param {string} projectRoot - Absolute path to project root
 * @param {string} outputFolder - Output folder name relative to project root
 * @returns {{ created: boolean, path: string, subdirs: string[] }}
 */
export function createOutputDirectory(projectRoot, outputFolder = '_spectra-output') {
  const outputPath = path.join(projectRoot, outputFolder);
  const createdDirs = [];

  // Create main output directory
  if (!fs.existsSync(outputPath)) {
    fs.mkdirSync(outputPath, { recursive: true });
  }
  createdDirs.push(outputFolder);

  // Create subdirectories
  for (const subdir of OUTPUT_SUBDIRS) {
    const subdirPath = path.join(outputPath, subdir);
    if (!fs.existsSync(subdirPath)) {
      fs.mkdirSync(subdirPath, { recursive: true });
    }
    createdDirs.push(`${outputFolder}/${subdir}`);
  }

  // Write a .gitkeep in each subdirectory so they're tracked
  for (const subdir of OUTPUT_SUBDIRS) {
    const gitkeepPath = path.join(outputPath, subdir, '.gitkeep');
    if (!fs.existsSync(gitkeepPath)) {
      fs.writeFileSync(gitkeepPath, '', 'utf-8');
    }
  }

  return { created: true, path: outputPath, subdirs: createdDirs };
}

// ---------------------------------------------------------------------------
// Initial Config Writing
// ---------------------------------------------------------------------------

/**
 * Write or update the SPECTRA core config.yaml with CLI-provided values.
 *
 * This replaces the need for interactive spectra-init on first use when
 * the user provides --user-name, --communication-language, etc.
 *
 * @param {string} spectraDir - Path to _spectra/ directory
 * @param {{ userName?: string, communicationLanguage?: string, documentOutputLanguage?: string, outputFolder?: string, modules?: string[], useDefaults?: boolean }} options
 * @returns {boolean} True if config was written/updated
 */
export function writeInitialConfig(spectraDir, options = {}) {
  const configPath = path.join(spectraDir, 'core', 'config.yaml');
  const configDir = path.dirname(configPath);

  // Only write if we have meaningful values to set
  const hasValues = options.userName ||
    options.communicationLanguage !== 'English' ||
    options.documentOutputLanguage !== 'English' ||
    options.outputFolder !== '_spectra-output' ||
    options.useDefaults;

  // Always write the config if useDefaults is set or we have explicit values
  if (!hasValues && !options.useDefaults) {
    // Check if config already exists
    if (fs.existsSync(configPath)) {
      return false; // Don't overwrite existing config with no new values
    }
  }

  // Read existing config if present
  let existingConfig = {};
  if (fs.existsSync(configPath)) {
    try {
      existingConfig = YAML.parse(fs.readFileSync(configPath, 'utf-8')) || {};
    } catch {
      existingConfig = {};
    }
  }

  // Merge new values into existing flat config (matches spectra_init.py format)
  const config = {
    ...existingConfig,
    user_name: options.userName || existingConfig.user_name || 'Operator',
    communication_language: options.communicationLanguage || existingConfig.communication_language || 'English',
    document_output_language: options.documentOutputLanguage || existingConfig.document_output_language || 'English',
    output_folder: options.outputFolder || existingConfig.output_folder || '_spectra-output',
    engagement_artifacts: existingConfig.engagement_artifacts || '{project-root}/_spectra-output/engagements',
    report_artifacts: existingConfig.report_artifacts || '{project-root}/_spectra-output/reports',
    evidence_artifacts: existingConfig.evidence_artifacts || '{project-root}/_spectra-output/evidence',
  };

  // Preserve context_budget if it exists
  if (existingConfig.context_budget) {
    config.context_budget = existingConfig.context_budget;
  }

  // Write config
  fs.mkdirSync(configDir, { recursive: true });
  const yamlContent = YAML.stringify(config, {
    lineWidth: 0,
    defaultStringType: 'QUOTE_DOUBLE',
    defaultKeyType: 'PLAIN',
  });

  fs.writeFileSync(configPath, yamlContent, 'utf-8');
  return true;
}

// ---------------------------------------------------------------------------
// Manifest
// ---------------------------------------------------------------------------

/**
 * Write or update the installation manifest.
 *
 * @param {string} spectraDir - Path to _spectra/ directory
 * @param {{ version: string, modules: string[], ides?: string[], previousVersion?: string, outputFolder?: string, userName?: string, communicationLanguage?: string, documentOutputLanguage?: string }} metadata
 */
export function writeManifest(spectraDir, metadata) {
  const configDir = path.join(spectraDir, '_config');
  fs.mkdirSync(configDir, { recursive: true });

  const manifestPath = path.join(configDir, 'manifest.yaml');
  const now = new Date().toISOString();

  // Read existing manifest for installDate preservation
  let existingInstallDate = now;
  if (fs.existsSync(manifestPath)) {
    try {
      const existing = YAML.parse(fs.readFileSync(manifestPath, 'utf-8'));
      existingInstallDate = existing?.installation?.installDate || now;
    } catch {
      // Use current date
    }
  }

  const manifest = {
    installation: {
      name: 'SPECTRA',
      fullName: 'Security Protocol Engineering for Cyber Threat Response & Assessment',
      claim: 'Attack. Defend. Evolve.',
      version: metadata.version,
      installDate: existingInstallDate,
      lastUpdated: now,
      outputFolder: metadata.outputFolder || '_spectra-output',
      ...(metadata.userName ? { userName: metadata.userName } : {}),
      ...(metadata.communicationLanguage ? { communicationLanguage: metadata.communicationLanguage } : {}),
      ...(metadata.documentOutputLanguage ? { documentOutputLanguage: metadata.documentOutputLanguage } : {}),
      ...(metadata.previousVersion ? { previousVersion: metadata.previousVersion } : {}),
    },
    modules: metadata.modules.map(mod => {
      const displayNames = {
        core: 'Core Framework',
        rtk:  'Red Team Kit',
        soc:  'Security Operations Center',
        irt:  'Incident Response Team',
        grc:  'Governance, Risk & Compliance',
      };
      return {
        name: mod,
        displayName: displayNames[mod] || mod.toUpperCase(),
        version: metadata.version,
        installDate: existingInstallDate,
        lastUpdated: now,
        source: 'built-in',
        npmPackage: null,
        repoUrl: null,
      };
    }),
    ides: metadata.ides || ['claude-code'],
  };

  const yamlContent = YAML.stringify(manifest, {
    lineWidth: 0,
    defaultStringType: 'QUOTE_DOUBLE',
    defaultKeyType: 'PLAIN',
  });

  fs.writeFileSync(manifestPath, yamlContent, 'utf-8');
}

/**
 * Read and parse the installation manifest.
 *
 * @param {string} spectraDir - Path to _spectra/ directory
 * @returns {Object|null}
 */
export function readManifest(spectraDir) {
  const manifestPath = path.join(spectraDir, '_config', 'manifest.yaml');
  if (!fs.existsSync(manifestPath)) return null;

  try {
    const content = fs.readFileSync(manifestPath, 'utf-8');
    return YAML.parse(content);
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Init Check
// ---------------------------------------------------------------------------

/**
 * Run a structural validation of the SPECTRA installation.
 *
 * Checks that critical directories and files exist.
 * If spectra_init.py is available, runs it for deeper validation.
 *
 * @param {string} spectraDir - Path to _spectra/ directory
 * @returns {{ success: boolean, message: string }}
 */
export function runInitCheck(spectraDir) {
  const errors = [];

  // Check critical structure
  const requiredDirs = ['core', '_config'];
  for (const dir of requiredDirs) {
    if (!fs.existsSync(path.join(spectraDir, dir))) {
      errors.push(`Missing directory: ${dir}`);
    }
  }

  const requiredFiles = ['SPECTRA.md', '_config/manifest.yaml'];
  for (const file of requiredFiles) {
    if (!fs.existsSync(path.join(spectraDir, file))) {
      errors.push(`Missing file: ${file}`);
    }
  }

  // Check for spectra_init.py
  const initScript = path.join(spectraDir, 'core', 'spectra-init', 'scripts', 'spectra_init.py');
  if (!fs.existsSync(initScript)) {
    errors.push('Missing: core/spectra-init/scripts/spectra_init.py');
  }

  if (errors.length > 0) {
    return { success: false, message: errors.join('; ') };
  }

  // Optionally try running spectra_init.py check
  try {
    const projectRoot = path.dirname(spectraDir);
    const result = execSync(
      `python3 "${initScript}" check --project-root "${projectRoot}"`,
      { encoding: 'utf-8', timeout: 10000, stdio: ['pipe', 'pipe', 'pipe'] }
    );
    // Parse output -- if it returns JSON with status, check it
    try {
      const parsed = JSON.parse(result.trim());
      if (parsed.status === 'no_project') {
        return { success: false, message: 'spectra_init.py: project not detected' };
      }
    } catch {
      // Non-JSON output is fine -- script ran successfully
    }
  } catch {
    // Python not available or script failed -- non-fatal, structural check passed
  }

  return { success: true, message: 'Installation verified' };
}

// ---------------------------------------------------------------------------
// Package Utilities
// ---------------------------------------------------------------------------

/**
 * Get the version from this package's package.json.
 *
 * @returns {string}
 */
export function getPackageVersion() {
  const pkgPath = path.resolve(__dirname, '..', 'package.json');
  try {
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
    return pkg.version || '0.0.0';
  } catch {
    return '0.0.0';
  }
}

/**
 * Get the source path for SPECTRA framework files.
 * This is the root of the npm package (where package.json lives).
 *
 * @returns {string}
 */
export function getSourcePath() {
  return path.resolve(__dirname, '..');
}
