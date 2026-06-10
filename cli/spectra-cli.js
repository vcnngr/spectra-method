#!/usr/bin/env node
/**
 * SPECTRA CLI -- Security Protocol Engineering for Cyber Threat Response & Assessment
 *
 * Usage:
 *   npx spectra-method install                              Install SPECTRA into current project
 *   npx spectra-method install --modules rtk,soc            Install specific modules only
 *   npx spectra-method install -d ./my-proj --tools claude-code,codex -y  Full options
 *   npx spectra-method validate                             Run project validation
 *   npx spectra-method status                               Show installation status
 *   npx spectra-method party plan --topic "..."             Generate Party Mode sub-agent plan
 *   npx spectra-method duel init --role red --session ENG   Initialize Duel Mode role
 *   npx spectra-method blue ingest --session ENG --source auth=/var/log/auth.log
 *   npx spectra-method broker export --session ENG --role red --bundle red.json
 *   npx spectra-method update                               Update SPECTRA to latest version
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { Command } from 'commander';
import chalk from 'chalk';
import {
  detectProjectRoot,
  checkExistingInstallation,
  copyFrameworkFiles,
  preserveUserConfigs,
  restoreUserConfigs,
  writeManifest,
  runInitCheck,
  readManifest,
  getPackageVersion,
  getSourcePath,
  registerSkillsForIDE,
  createOutputDirectory,
  writeInitialConfig,
} from './installer.js';

const BANNER = `
${chalk.red('  ███████╗██████╗ ███████╗ ██████╗████████╗██████╗  █████╗ ')}
${chalk.red('  ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗')}
${chalk.yellow('  ███████╗██████╔╝█████╗  ██║        ██║   ██████╔╝███████║')}
${chalk.yellow('  ╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══██╗██╔══██║')}
${chalk.blue('  ███████║██║     ███████╗╚██████╗   ██║   ██║  ██║██║  ██║')}
${chalk.blue('  ╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝')}
${chalk.gray('  Security Protocol Engineering for Cyber Threat Response & Assessment')}
${chalk.gray('  "Attack. Defend. Evolve."')}
`;

const ALL_MODULES = ['core', 'rtk', 'soc', 'irt', 'grc'];

const MODULE_INFO = {
  core: { icon: '\u26A1', name: 'Core Framework', agents: 3, skills: 11 },
  rtk:  { icon: '\uD83D\uDD34', name: 'Red Team Kit', agents: 7, workflows: 6 },
  soc:  { icon: '\uD83D\uDD35', name: 'Security Operations Center', agents: 8, workflows: 6 },
  irt:  { icon: '\uD83D\uDFE0', name: 'Incident Response Team', agents: 6, workflows: 5 },
  grc:  { icon: '\u26AA', name: 'Governance, Risk & Compliance', agents: 4, workflows: 4 },
};

const SUPPORTED_IDES = ['claude-code', 'codex', 'cursor'];

function getExecutionScript(targetRoot, scriptName) {
  const installedPath = path.join(targetRoot, '_spectra', 'core', 'execution', scriptName);
  if (fs.existsSync(installedPath)) {
    return installedPath;
  }
  return path.join(getSourcePath(), 'core', 'execution', scriptName);
}

function getOutputFolder(targetRoot) {
  const manifest = readManifest(path.join(targetRoot, '_spectra'));
  return manifest?.installation?.outputFolder || '_spectra-output';
}

function getDuelOutputRoot(targetRoot) {
  return path.join(targetRoot, getOutputFolder(targetRoot), 'duel');
}

function parseModuleList(value) {
  if (!value) return [];
  return value.split(',').map(m => m.trim().toLowerCase()).filter(Boolean);
}

function validateModules(modules) {
  const invalidModules = modules.filter(m => !ALL_MODULES.includes(m));
  if (invalidModules.length > 0) {
    console.error(chalk.red(`\n  Unknown module(s): ${invalidModules.join(', ')}`));
    console.error(chalk.gray(`  Available modules: ${ALL_MODULES.join(', ')}\n`));
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// CLI Definition
// ---------------------------------------------------------------------------

const program = new Command();

program
  .name('spectra')
  .description('SPECTRA -- Multi-agent cybersecurity framework')
  .version(getPackageVersion());

// --- install ---------------------------------------------------------------
program
  .command('install')
  .description('Install SPECTRA into a project')
  .option('-d, --directory <path>', 'Installation directory (default: current directory)')
  .option('-t, --target <path>', 'Alias for --directory (backwards compat)')
  .option('-m, --modules <modules>', 'Comma-separated module IDs (e.g., "rtk,soc")')
  .option('--lazy', 'Install only core now; add modules later with "spectra modules add"')
  .option('--tools <tools>', 'Comma-separated IDE IDs (e.g., "claude-code,codex"). Use "none" to skip.', 'claude-code')
  .option('--user-name <name>', 'Name for agents to use')
  .option('--communication-language <lang>', 'Language for agent communication', 'English')
  .option('--document-output-language <lang>', 'Language for document output', 'English')
  .option('--output-folder <path>', 'Output folder relative to project root', '_spectra-output')
  .option('--action <type>', 'Action: install, update, or quick-update', 'install')
  .option('-y, --yes', 'Accept all defaults, skip prompts')
  .option('-f, --force', 'Force reinstall over existing installation')
  .option('--custom-content <paths>', 'Custom modules/agents/workflows (comma-separated paths)')
  .action(async (options) => {
    console.log(BANNER);

    // Route to update if --action specifies it
    if (options.action === 'update' || options.action === 'quick-update') {
      console.log(chalk.gray(`  Routing to ${options.action} action...\n`));
      // Fall through to install logic but with update semantics
      options.force = true;
    }

    // --directory takes precedence; --target is backwards compat alias
    const targetDir = options.directory || options.target;
    const targetRoot = detectProjectRoot(targetDir);
    const sourcePath = getSourcePath();
    const spectraDir = `${targetRoot}/_spectra`;

    // Determine which modules to install
    const requestedModules = options.lazy
      ? ['core']
      : (options.modules ? parseModuleList(options.modules) : ALL_MODULES);

    // Validate module names
    validateModules(requestedModules);

    // Ensure core is always included
    if (!requestedModules.includes('core')) {
      requestedModules.unshift('core');
    }

    // Parse --tools
    const toolsList = options.tools === 'none'
      ? []
      : options.tools.split(',').map(t => t.trim().toLowerCase());

    // Validate IDE names
    const invalidIdes = toolsList.filter(t => !SUPPORTED_IDES.includes(t));
    if (invalidIdes.length > 0) {
      console.error(chalk.red(`\n  Unknown IDE(s): ${invalidIdes.join(', ')}`));
      console.error(chalk.gray(`  Supported IDEs: ${SUPPORTED_IDES.join(', ')}, or "none" to skip`));
      process.exit(1);
    }

    console.log(chalk.white('\n  Target:     ') + chalk.cyan(targetRoot));
    console.log(chalk.white('  Modules:    ') + chalk.cyan(requestedModules.join(', ')));
    console.log(chalk.white('  IDE tools:  ') + chalk.cyan(toolsList.length > 0 ? toolsList.join(', ') : 'none'));
    console.log(chalk.white('  Output dir: ') + chalk.cyan(options.outputFolder));
    if (options.userName) {
      console.log(chalk.white('  User name:  ') + chalk.cyan(options.userName));
    }
    console.log();

    // -----------------------------------------------------------------------
    // Step 1: Check existing installation
    // -----------------------------------------------------------------------
    console.log(chalk.gray('  [1/6] Checking existing installation...'));
    const existing = checkExistingInstallation(spectraDir);
    if (existing.exists && !options.force) {
      console.log(chalk.yellow('  Existing SPECTRA installation detected.'));
      console.log(chalk.gray(`  Version: ${existing.version || 'unknown'}`));
      console.log(chalk.gray(`  Installed: ${existing.installDate || 'unknown'}`));
      console.log();
      console.log(chalk.white('  Upgrading -- user configs will be preserved.'));
      console.log();
    }

    // Preserve user configs if updating
    let savedConfigs = null;
    if (existing.exists) {
      savedConfigs = preserveUserConfigs(spectraDir);
      console.log(chalk.green(`  \u2713 Backed up ${savedConfigs.count} config file(s)`));
    } else {
      console.log(chalk.green('  \u2713 Fresh installation'));
    }

    // -----------------------------------------------------------------------
    // Step 2: Copy framework files
    // -----------------------------------------------------------------------
    console.log(chalk.gray('  [2/6] Copying framework files...'));
    const copyResult = copyFrameworkFiles(sourcePath, spectraDir, {
      modules: requestedModules,
    });

    // Restore user configs if they were backed up
    if (savedConfigs && savedConfigs.count > 0) {
      restoreUserConfigs(spectraDir, savedConfigs);
    }

    console.log(chalk.green(`  \u2713 ${copyResult.fileCount} files`));

    // -----------------------------------------------------------------------
    // Step 3: Create output directory
    // -----------------------------------------------------------------------
    console.log(chalk.gray('  [3/6] Creating output directory...'));
    const outputResult = createOutputDirectory(targetRoot, options.outputFolder);
    console.log(chalk.green(`  \u2713 ${options.outputFolder}/`));

    // -----------------------------------------------------------------------
    // Step 4: Write configuration
    // -----------------------------------------------------------------------
    console.log(chalk.gray('  [4/6] Writing configuration...'));
    const configWritten = writeInitialConfig(spectraDir, {
      userName: options.userName,
      communicationLanguage: options.communicationLanguage,
      documentOutputLanguage: options.documentOutputLanguage,
      outputFolder: options.outputFolder,
      modules: requestedModules,
      useDefaults: options.yes || false,
    });
    if (configWritten) {
      console.log(chalk.green('  \u2713 config.yaml updated'));
    } else {
      console.log(chalk.green('  \u2713 config.yaml unchanged'));
    }

    // -----------------------------------------------------------------------
    // Step 5: Register skills for IDE
    // -----------------------------------------------------------------------
    if (toolsList.length > 0) {
      for (const ide of toolsList) {
        console.log(chalk.gray(`  [5/6] Registering skills for ${ide}...`));
        const skillResult = registerSkillsForIDE(targetRoot, ide, {
          modules: requestedModules,
          spectraDir,
        });
        const label = ide === 'codex'
          ? '.codex/spectra/ + AGENTS.md'
          : ide === 'claude-code'
            ? '.claude/skills/'
            : `.${ide}/skills/`;
        console.log(chalk.green(`  \u2713 ${skillResult.registered} skills registered for ${ide} in ${label}`));
      }
    } else {
      console.log(chalk.gray('  [5/6] Skipping skill registration (--tools none)'));
    }

    // -----------------------------------------------------------------------
    // Step 6: Finalize -- write manifest and verify
    // -----------------------------------------------------------------------
    console.log(chalk.gray('  [6/6] Finalizing...'));
    writeManifest(spectraDir, {
      version: getPackageVersion(),
      modules: requestedModules,
      ides: toolsList,
      outputFolder: options.outputFolder,
      userName: options.userName,
      communicationLanguage: options.communicationLanguage,
      documentOutputLanguage: options.documentOutputLanguage,
    });

    const initResult = runInitCheck(spectraDir);
    if (initResult.success) {
      console.log(chalk.green('  \u2713 manifest.yaml written'));
    } else {
      console.log(chalk.yellow(`  \u26A0 ${initResult.message}`));
    }

    // -----------------------------------------------------------------------
    // Success output
    // -----------------------------------------------------------------------
    console.log(chalk.green.bold('\n  SPECTRA installed successfully.\n'));
    console.log(chalk.white('  Installed modules:'));
    for (const mod of requestedModules) {
      const info = MODULE_INFO[mod];
      const detail = info.workflows
        ? `${info.agents} agents, ${info.workflows} workflows`
        : `${info.agents} agents, ${info.skills} skills`;
      console.log(`    ${info.icon}  ${chalk.bold(mod.toUpperCase())} -- ${info.name} (${detail})`);
    }

    console.log(chalk.white('\n  Next steps:'));
    console.log(chalk.gray('    1. Run the spectra-init skill to configure your project'));
    console.log(chalk.gray('    2. Create an engagement with spectra-new-engagement'));
    console.log(chalk.gray('    3. Invoke agents: "Talk to Viper" (red team), "Talk to Commander" (SOC)'));
    console.log(chalk.gray(`\n    npx spectra-method validate    Verify the installation`));
    console.log(chalk.gray(`    npx spectra-method status      View installation details\n`));
  });

// --- validate --------------------------------------------------------------
program
  .command('validate')
  .description('Validate SPECTRA installation')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('-t, --target <path>', 'Alias for --directory (backwards compat)')
  .option('--deep', 'Run the full Python validator in addition to CLI checks')
  .action(async (options) => {
    console.log(BANNER);

    const targetDir = options.directory || options.target;
    const targetRoot = detectProjectRoot(targetDir);
    const spectraDir = `${targetRoot}/_spectra`;

    const existing = checkExistingInstallation(spectraDir);
    if (!existing.exists) {
      console.error(chalk.red('\n  No SPECTRA installation found.'));
      console.error(chalk.gray('  Run: npx spectra-method install\n'));
      process.exit(1);
    }

    console.log(chalk.white('\n  Validating SPECTRA installation...\n'));

    const initResult = runInitCheck(spectraDir);
    if (initResult.success) {
      console.log(chalk.green('  \u2713 Installation structure valid'));
    } else {
      console.log(chalk.red(`  \u2717 Structure check failed: ${initResult.message}`));
    }

    // Check each module directory
    const manifest = readManifest(spectraDir);
    const installedModules = manifest?.modules?.map(m => m.name) || ALL_MODULES;

    let allValid = true;
    for (const mod of installedModules) {
      const modPath = `${spectraDir}/${mod === 'core' ? 'core' : mod}`;
      if (fs.existsSync(modPath)) {
        console.log(chalk.green(`  \u2713 Module ${mod.toUpperCase()} present`));
      } else {
        console.log(chalk.red(`  \u2717 Module ${mod.toUpperCase()} missing`));
        allValid = false;
      }
    }

    // Check config files
    for (const mod of installedModules) {
      const configPath = `${spectraDir}/${mod === 'core' ? 'core' : mod}/config.yaml`;
      if (fs.existsSync(configPath)) {
        console.log(chalk.green(`  \u2713 Config ${mod}.config.yaml present`));
      } else {
        console.log(chalk.yellow(`  \u26A0 Config ${mod}.config.yaml missing (run spectra-init)`));
      }
    }

    // Check framework files
    const frameworkFiles = ['SPECTRA.md', '_config/manifest.yaml'];
    for (const file of frameworkFiles) {
      if (fs.existsSync(`${spectraDir}/${file}`)) {
        console.log(chalk.green(`  \u2713 ${file}`));
      } else {
        console.log(chalk.red(`  \u2717 ${file} missing`));
        allValid = false;
      }
    }

    // Check skill registration
    const installedIdes = manifest?.ides || [];
    const skillsDir = `${targetRoot}/.claude/skills`;
    if (fs.existsSync(skillsDir)) {
      const skillDirs = fs.readdirSync(skillsDir).filter(d =>
        d.startsWith('spectra-') && fs.statSync(`${skillsDir}/${d}`).isDirectory()
      );
      console.log(chalk.green(`  \u2713 ${skillDirs.length} skills registered in .claude/skills/`));
    } else if (installedIdes.includes('claude-code') || installedIdes.length === 0) {
      console.log(chalk.yellow('  \u26A0 No .claude/skills/ directory (run install with --tools claude-code)'));
    }

    if (installedIdes.includes('codex')) {
      const codexIndex = `${targetRoot}/.codex/spectra/skill-index.json`;
      const codexAgents = `${targetRoot}/AGENTS.md`;
      if (fs.existsSync(codexIndex) && fs.existsSync(codexAgents)) {
        const codexSkills = JSON.parse(fs.readFileSync(codexIndex, 'utf-8')).skills || [];
        console.log(chalk.green(`  \u2713 ${codexSkills.length} skills indexed for Codex in .codex/spectra/`));
      } else {
        console.log(chalk.yellow('  \u26A0 Codex adapter incomplete (run install with --tools codex)'));
      }
    }

    // Check output directory
    const outputDir = manifest?.installation?.outputFolder || '_spectra-output';
    if (fs.existsSync(`${targetRoot}/${outputDir}`)) {
      console.log(chalk.green(`  \u2713 Output directory ${outputDir}/ present`));
    } else {
      console.log(chalk.yellow(`  \u26A0 Output directory ${outputDir}/ missing`));
    }

    if (options.deep) {
      console.log(chalk.white('\n  Deep validation'));
      console.log(chalk.gray('  ----------------------------------------'));
      const validatorPath = path.join(getSourcePath(), 'core', 'execution', 'validate-spectra.py');
      if (!fs.existsSync(validatorPath)) {
        console.log(chalk.yellow('  \u26A0 Full validator not available in this package'));
      } else {
        try {
          execFileSync('python3', [validatorPath, '--path', targetRoot, '--strict', '--summary'], {
            stdio: 'inherit',
          });
          console.log(chalk.green('  \u2713 Full validator passed'));
        } catch {
          console.log(chalk.red('  \u2717 Full validator failed'));
          allValid = false;
        }
      }
    }

    console.log();
    if (allValid) {
      console.log(chalk.green.bold('  Validation passed.\n'));
    } else {
      console.log(chalk.yellow.bold('  Validation completed with warnings.\n'));
      console.log(chalk.gray('  Run: npx spectra-method install --force   to repair\n'));
    }
  });

// --- modules ---------------------------------------------------------------
program
  .command('modules')
  .description('List or lazily add SPECTRA modules')
  .argument('<action>', 'list or add')
  .argument('[modules]', 'Comma-separated modules for add, e.g. rtk,soc')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('-t, --target <path>', 'Alias for --directory (backwards compat)')
  .option('--tools <tools>', 'Comma-separated IDE IDs (e.g., "claude-code,codex"). Use "none" to skip.', 'claude-code')
  .action((action, modulesArg, options) => {
    const targetDir = options.directory || options.target;
    const targetRoot = detectProjectRoot(targetDir);
    const spectraDir = `${targetRoot}/_spectra`;
    const existing = checkExistingInstallation(spectraDir);
    if (!existing.exists) {
      console.error(chalk.red('\n  No SPECTRA installation found.'));
      console.error(chalk.gray('  Run: npx spectra-method install --lazy\n'));
      process.exit(1);
    }

    const manifest = readManifest(spectraDir) || {};
    const installedModules = manifest.modules?.map(m => m.name) || ['core'];

    if (action === 'list') {
      console.log(chalk.white('\n  SPECTRA modules'));
      console.log(chalk.gray('  ----------------------------------------'));
      for (const mod of ALL_MODULES) {
        const installed = installedModules.includes(mod);
        const marker = installed ? chalk.green('installed') : chalk.gray('available');
        const info = MODULE_INFO[mod];
        console.log(`  ${info.icon}  ${mod.padEnd(6)} ${marker}`);
      }
      console.log();
      return;
    }

    if (action !== 'add') {
      console.error(chalk.red(`\n  Unknown modules action: ${action}`));
      console.error(chalk.gray('  Valid actions: list, add\n'));
      process.exit(1);
    }

    const requestedModules = parseModuleList(modulesArg);
    if (requestedModules.length === 0) {
      console.error(chalk.red('\n  No modules specified.'));
      console.error(chalk.gray('  Run: npx spectra-method modules add rtk,soc\n'));
      process.exit(1);
    }
    validateModules(requestedModules);

    const newModules = requestedModules.filter(m => !installedModules.includes(m));
    if (newModules.length === 0) {
      console.log(chalk.green('\n  Requested modules already installed.\n'));
      return;
    }

    const updatedModules = [...installedModules, ...newModules];
    console.log(chalk.white('\n  Adding modules: ') + chalk.cyan(newModules.join(', ')));
    const sourcePath = getSourcePath();
    const copyResult = copyFrameworkFiles(sourcePath, spectraDir, { modules: newModules });
    console.log(chalk.green(`  \u2713 Copied ${copyResult.fileCount} files`));

    writeInitialConfig(spectraDir, {
      modules: newModules,
      outputFolder: manifest.installation?.outputFolder || '_spectra-output',
      userName: manifest.installation?.userName,
      communicationLanguage: manifest.installation?.communicationLanguage,
      documentOutputLanguage: manifest.installation?.documentOutputLanguage,
      useDefaults: true,
    });

    const toolsList = options.tools === 'none'
      ? []
      : options.tools.split(',').map(t => t.trim().toLowerCase());
    const invalidIdes = toolsList.filter(t => !SUPPORTED_IDES.includes(t));
    if (invalidIdes.length > 0) {
      console.error(chalk.red(`\n  Unknown IDE(s): ${invalidIdes.join(', ')}`));
      process.exit(1);
    }

    if (toolsList.length > 0) {
      for (const ide of toolsList) {
        const skillResult = registerSkillsForIDE(targetRoot, ide, {
          modules: updatedModules,
          spectraDir,
        });
        console.log(chalk.green(`  \u2713 Registered ${skillResult.registered} skills for ${ide}`));
      }
    }

    writeManifest(spectraDir, {
      version: getPackageVersion(),
      modules: updatedModules,
      ides: toolsList,
      previousVersion: manifest.installation?.version,
      outputFolder: manifest.installation?.outputFolder || '_spectra-output',
      userName: manifest.installation?.userName,
      communicationLanguage: manifest.installation?.communicationLanguage,
      documentOutputLanguage: manifest.installation?.documentOutputLanguage,
    });
    console.log(chalk.green.bold('\n  Modules added.\n'));
  });

// --- engagement ------------------------------------------------------------
program
  .command('engagement')
  .description('Run deterministic engagement validation, gate, status, or transition')
  .argument('<action>', 'validate, status, gate, or transition')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('-t, --target <path>', 'Alias for --directory (backwards compat)')
  .requiredOption('-e, --engagement <path>', 'Path to engagement.yaml')
  .option('-w, --workflow <name>', 'RTK workflow name for gate/transition')
  .option('--target-name <target>', 'Target to verify through scope-enforcer')
  .option('--action-type <type>', 'Action override for gate/transition')
  .option('--to <status>', 'Destination workflow status for transition')
  .option('--agent <name>', 'Agent name for transition metadata')
  .option('--artifact <path>', 'Artifact path for transition metadata', (value, previous) => {
    previous.push(value);
    return previous;
  }, [])
  .option('--findings-count <count>', 'Finding count for transition metadata')
  .option('--strict', 'Strict validation')
  .option('--force', 'Force transition despite invalid state/gate')
  .option('--dry-run', 'Do not write transition updates')
  .action((action, options) => {
    const targetDir = options.directory || options.target;
    const targetRoot = detectProjectRoot(targetDir);
    const script = getExecutionScript(targetRoot, 'engagement-state.py');

    if (!fs.existsSync(script)) {
      console.error(chalk.red(`\n  engagement-state.py not found: ${script}\n`));
      process.exit(1);
    }

    const allowed = new Set(['validate', 'status', 'gate', 'transition']);
    if (!allowed.has(action)) {
      console.error(chalk.red(`\n  Unknown engagement action: ${action}`));
      console.error(chalk.gray('  Valid actions: validate, status, gate, transition\n'));
      process.exit(1);
    }

    const args = [script, action, '--engagement', options.engagement];
    if (options.strict) args.push('--strict');
    if (options.workflow) args.push('--workflow', options.workflow);
    if (options.targetName) args.push('--target', options.targetName);
    if (options.actionType) args.push('--action', options.actionType);
    if (options.to) args.push('--to', options.to);
    if (options.agent) args.push('--agent', options.agent);
    if (options.findingsCount) args.push('--findings-count', options.findingsCount);
    for (const artifact of options.artifact || []) {
      args.push('--artifact', artifact);
    }
    if (options.force) args.push('--force');
    if (options.dryRun) args.push('--dry-run');

    try {
      execFileSync('python3', args, { stdio: 'inherit' });
    } catch (error) {
      process.exit(error.status || 1);
    }
  });

// --- runs (run accounting) -------------------------------------------------
program
  .command('runs')
  .description('Show the per-engagement run log: what gated tools ran and their outcomes')
  .argument('[action]', 'status or path', 'status')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .requiredOption('-e, --engagement <path>', 'Path to engagement.yaml')
  .option('--limit <n>', 'How many recent runs to include (status)', '10')
  .action((action, options) => {
    const targetRoot = detectProjectRoot(options.directory);
    const script = getExecutionScript(targetRoot, 'run-accounting.py');

    if (!fs.existsSync(script)) {
      console.error(chalk.red(`\n  run-accounting.py not found: ${script}\n`));
      process.exit(1);
    }

    const allowed = new Set(['status', 'path']);
    if (!allowed.has(action)) {
      console.error(chalk.red(`\n  Unknown runs action: ${action}`));
      console.error(chalk.gray('  Valid actions: status, path\n'));
      process.exit(1);
    }

    const args = [script, action, '--engagement', options.engagement];
    if (action === 'status') args.push('--limit', options.limit);

    try {
      execFileSync('python3', args, { stdio: 'inherit' });
    } catch (error) {
      process.exit(error.status || 1);
    }
  });

// --- posture (recurring engagement posture diff) ---------------------------
program
  .command('posture')
  .description('Snapshot an engagement posture and diff snapshots over time')
  .argument('[action]', 'snapshot, diff, or list', 'diff')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .requiredOption('-e, --engagement <path>', 'Path to engagement.yaml')
  .option('--from <path>', 'Older snapshot JSON (diff)')
  .option('--to <path>', 'Newer snapshot JSON (diff)')
  .action((action, options) => {
    const targetRoot = detectProjectRoot(options.directory);
    const script = getExecutionScript(targetRoot, 'posture-diff.py');
    if (!fs.existsSync(script)) {
      console.error(chalk.red(`\n  posture-diff.py not found: ${script}\n`));
      process.exit(1);
    }
    const allowed = new Set(['snapshot', 'diff', 'list']);
    if (!allowed.has(action)) {
      console.error(chalk.red(`\n  Unknown posture action: ${action}`));
      console.error(chalk.gray('  Valid actions: snapshot, diff, list\n'));
      process.exit(1);
    }
    const args = [script, action, '--engagement', options.engagement];
    if (action === 'diff' && options.from) args.push('--from', options.from);
    if (action === 'diff' && options.to) args.push('--to', options.to);
    try {
      execFileSync('python3', args, { stdio: 'inherit' });
    } catch (error) {
      process.exit(error.status || 1);
    }
  });

// --- export (remediation-ready findings export) ----------------------------
program
  .command('export')
  .description('Export engagement findings as sarif, csv, or md (remediation-ready)')
  .requiredOption('-e, --engagement <path>', 'Path to engagement.yaml')
  .requiredOption('-f, --format <fmt>', 'sarif, csv, or md')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('-o, --out <path>', 'Write to file instead of stdout')
  .action((options) => {
    const targetRoot = detectProjectRoot(options.directory);
    const script = getExecutionScript(targetRoot, 'remediation-export.py');
    if (!fs.existsSync(script)) {
      console.error(chalk.red(`\n  remediation-export.py not found: ${script}\n`));
      process.exit(1);
    }
    const args = [script, 'export', '--engagement', options.engagement,
                  '--format', options.format];
    if (options.out) args.push('--out', options.out);
    try {
      execFileSync('python3', args, { stdio: 'inherit' });
    } catch (error) {
      process.exit(error.status || 1);
    }
  });

// --- quickstart (onboarding: scaffold a demo/scenario engagement) ----------
program
  .command('quickstart')
  .description('Scaffold a ready-to-run demo (or scenario) engagement and print a guided tour')
  .argument('[action]', 'init or list', 'init')
  .option('-t, --template <name>', 'demo, web-pentest, cloud-ir, ot-assessment', 'demo')
  .option('--dest <dir>', 'Destination directory', './spectra-quickstart')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('--force', 'Overwrite an existing engagement.yaml')
  .action((action, options) => {
    const targetRoot = detectProjectRoot(options.directory);
    const script = getExecutionScript(targetRoot, 'quickstart.py');
    if (!fs.existsSync(script)) {
      console.error(chalk.red(`\n  quickstart.py not found: ${script}\n`));
      process.exit(1);
    }
    if (action === 'list') {
      try {
        execFileSync('python3', [script, 'list'], { stdio: 'inherit' });
      } catch (error) {
        process.exit(error.status || 1);
      }
      return;
    }
    if (action !== 'init') {
      console.error(chalk.red(`\n  Unknown quickstart action: ${action}`));
      console.error(chalk.gray('  Valid actions: init, list\n'));
      process.exit(1);
    }
    const args = [script, 'init', '--template', options.template, '--dest', options.dest];
    if (options.force) args.push('--force');
    try {
      const out = execFileSync('python3', args, { encoding: 'utf8' });
      const m = JSON.parse(out);
      console.log(chalk.bold(`\n  SPECTRA quickstart — ${m.template}\n`));
      console.log(chalk.gray(`  Scaffolded ${m.files.length} file(s) into ${m.dest}\n`));
      m.tour.forEach((step, i) => console.log(`  ${chalk.cyan(String(i + 1) + '.')} ${step}`));
      console.log(chalk.gray('\n  Authorized-only, evidence-gated. The demo targets loopback only.\n'));
    } catch (error) {
      if (error.stdout) process.stdout.write(error.stdout);
      if (error.stderr) process.stderr.write(error.stderr);
      process.exit(error.status || 1);
    }
  });

// --- report ---------------------------------------------------------------
program
  .command('report')
  .description('Generate a structured report from engagement adapters')
  .argument('<action>', 'generate')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('-t, --target <path>', 'Alias for --directory (backwards compat)')
  .requiredOption('-e, --engagement <path>', 'Path to engagement.yaml')
  .option('--type <type>', 'Report type: pentest, incident, compliance, executive, custom', 'pentest')
  .option('-o, --output <path>', 'Output report path')
  .action((action, options) => {
    if (action !== 'generate') {
      console.error(chalk.red(`\n  Unknown report action: ${action}`));
      console.error(chalk.gray('  Valid actions: generate\n'));
      process.exit(1);
    }
    const targetDir = options.directory || options.target;
    const targetRoot = detectProjectRoot(targetDir);
    const script = getExecutionScript(targetRoot, 'report-generator.py');
    const args = [script, 'generate', '--engagement', options.engagement, '--type', options.type];
    if (options.output) args.push('--output', options.output);
    try {
      execFileSync('python3', args, { stdio: 'inherit' });
    } catch (error) {
      process.exit(error.status || 1);
    }
  });

// --- party ----------------------------------------------------------------
program
  .command('party')
  .description('Generate deterministic Party Mode sub-agent plans')
  .argument('<action>', 'plan')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('-t, --target <path>', 'Alias for --directory (backwards compat)')
  .requiredOption('--topic <topic>', 'Discussion or task topic')
  .option('--mode <mode>', 'adversarial, collaborative, purple, or incident', 'adversarial')
  .option('--agents-per-team <count>', 'Number of agents per required team', '1')
  .option('--lanes <lanes>', 'Comma-separated lanes to require, e.g. red,blue,irt,grc,core')
  .option('--format <format>', 'json or markdown', 'json')
  .option('-o, --output <path>', 'Output plan path')
  .action((action, options) => {
    if (action !== 'plan') {
      console.error(chalk.red(`\n  Unknown party action: ${action}`));
      console.error(chalk.gray('  Valid actions: plan\n'));
      process.exit(1);
    }
    const targetDir = options.directory || options.target;
    const targetRoot = detectProjectRoot(targetDir);
    const script = getExecutionScript(targetRoot, 'party-orchestrator.py');
    const installedManifest = path.join(targetRoot, '_spectra', '_config', 'agent-manifest.csv');
    const sourceManifest = path.join(getSourcePath(), '_config', 'agent-manifest.csv');
    const manifest = fs.existsSync(installedManifest) ? installedManifest : sourceManifest;
    const installedConfig = path.join(targetRoot, '_spectra', 'core', 'config.yaml');
    const sourceConfig = path.join(getSourcePath(), 'core', 'config.yaml');
    const config = fs.existsSync(installedConfig) ? installedConfig : sourceConfig;
    const manifestYaml = readManifest(path.join(targetRoot, '_spectra'));
    const modules = manifestYaml?.modules?.map(m => m.name).filter(Boolean).join(',');
    const args = [
      script,
      'plan',
      '--topic',
      options.topic,
      '--mode',
      options.mode,
      '--agents-per-team',
      options.agentsPerTeam,
      '--format',
      options.format,
      '--manifest',
      manifest,
      '--config',
      config,
    ];
    if (modules) args.push('--modules', modules);
    if (options.lanes) args.push('--lanes', options.lanes);
    if (options.output) args.push('--output', options.output);
    try {
      execFileSync('python3', args, { stdio: 'inherit' });
    } catch (error) {
      process.exit(error.status || 1);
    }
  });

// --- duel -----------------------------------------------------------------
program
  .command('duel')
  .description('Run Duel Mode role ledgers and Red/Blue scoring')
  .argument('<action>', 'init, record, status, or score')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('-t, --target <path>', 'Alias for --directory (backwards compat)')
  .requiredOption('--session <id>', 'Duel session or engagement ID')
  .option('--role <role>', 'red, blue, or referee')
  .option('-e, --engagement <path>', 'Path to engagement.yaml')
  .option('--event-type <type>', 'Role event type for record')
  .option('--summary <text>', 'Event summary for record')
  .option('--target-name <target>', 'Target associated with the event')
  .option('--technique <technique>', 'ATT&CK technique or local technique label')
  .option('--source <source>', 'Telemetry source, tool, or evidence source')
  .option('--confidence <level>', 'low, medium, or high', 'medium')
  .option('--severity <level>', 'low, medium, high, or critical', 'medium')
  .option('--red-event-id <id>', 'Red event ID correlated by a Blue/Referee event')
  .option('--artifact <path>', 'Artifact path to attach to the event', (value, previous) => {
    previous.push(value);
    return previous;
  }, [])
  .option('--format <format>', 'json or markdown for score', 'markdown')
  .option('-o, --output <path>', 'Output scorecard path')
  .action((action, options) => {
    const targetDir = options.directory || options.target;
    const targetRoot = detectProjectRoot(targetDir);
    const script = getExecutionScript(targetRoot, 'duel-orchestrator.py');
    const outputRoot = getDuelOutputRoot(targetRoot);

    const args = [script, action, '--session', options.session];

    if (action === 'init') {
      if (!options.role) {
        console.error(chalk.red('\n  --role is required for duel init\n'));
        process.exit(1);
      }
      args.push('--role', options.role, '--output-root', outputRoot);
      if (options.engagement) args.push('--engagement', options.engagement);
    } else if (action === 'record') {
      if (!options.role || !options.eventType || !options.summary) {
        console.error(chalk.red('\n  --role, --event-type, and --summary are required for duel record\n'));
        process.exit(1);
      }
      args.push(
        '--role', options.role,
        '--event-type', options.eventType,
        '--summary', options.summary,
        '--output-root', outputRoot,
        '--confidence', options.confidence,
        '--severity', options.severity,
      );
      if (options.targetName) args.push('--target', options.targetName);
      if (options.technique) args.push('--technique', options.technique);
      if (options.source) args.push('--source', options.source);
      if (options.redEventId) args.push('--red-event-id', options.redEventId);
      for (const artifact of options.artifact || []) {
        args.push('--artifact', artifact);
      }
    } else if (action === 'status') {
      args.push('--output-root', outputRoot);
    } else if (action === 'score') {
      const redLedger = path.join(outputRoot, options.session, 'red', 'red-events.jsonl');
      const blueLedger = path.join(outputRoot, options.session, 'blue', 'blue-events.jsonl');
      args.push('--red', redLedger, '--blue', blueLedger, '--format', options.format);
      if (options.output) args.push('--output', options.output);
    } else {
      console.error(chalk.red(`\n  Unknown duel action: ${action}`));
      console.error(chalk.gray('  Valid actions: init, record, status, score\n'));
      process.exit(1);
    }

    try {
      execFileSync('python3', args, { stdio: 'inherit' });
    } catch (error) {
      process.exit(error.status || 1);
    }
  });

// --- blue -----------------------------------------------------------------
program
  .command('blue')
  .description('Ingest Blue Team telemetry into Duel Mode')
  .argument('<action>', 'ingest or tail')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('-t, --target <path>', 'Alias for --directory (backwards compat)')
  .requiredOption('--session <id>', 'Duel session or engagement ID')
  .option('--source <type=path>', 'Telemetry source, e.g. auth=/var/log/auth.log', (value, previous) => {
    previous.push(value);
    return previous;
  }, [])
  .option('--dry-run', 'Parse and print detections without writing the Blue ledger')
  .option('--once', 'For tail mode, process newly appended data once and exit')
  .option('--checkpoint <path>', 'For tail mode, checkpoint file for source offsets')
  .option('--format <format>', 'json or jsonl for dry-run output', 'json')
  .action((action, options) => {
    if (!['ingest', 'tail'].includes(action)) {
      console.error(chalk.red(`\n  Unknown blue action: ${action}`));
      console.error(chalk.gray('  Valid actions: ingest, tail\n'));
      process.exit(1);
    }
    if (!options.source || options.source.length === 0) {
      console.error(chalk.red('\n  At least one --source type=path is required\n'));
      process.exit(1);
    }
    const targetDir = options.directory || options.target;
    const targetRoot = detectProjectRoot(targetDir);
    const script = getExecutionScript(targetRoot, 'blue-live-adapter.py');
    const outputRoot = getDuelOutputRoot(targetRoot);
    const args = [script, action, '--session', options.session, '--output-root', outputRoot, '--format', options.format];
    for (const source of options.source) {
      args.push('--source', source);
    }
    if (options.dryRun) args.push('--dry-run');
    if (options.once) args.push('--once');
    if (action === 'tail') {
      const checkpoint = options.checkpoint
        || path.join(outputRoot, options.session, 'blue', 'blue-tail.checkpoint.json');
      args.push('--checkpoint', checkpoint);
    } else if (options.checkpoint) {
      console.error(chalk.yellow('  Warning: --checkpoint is only used by blue tail; ignoring for blue ingest.'));
    }
    try {
      execFileSync('python3', args, { stdio: 'inherit' });
    } catch (error) {
      process.exit(error.status || 1);
    }
  });

// --- broker ---------------------------------------------------------------
program
  .command('broker')
  .description('Export/import Duel Mode ledgers for separated Red/Blue machines')
  .argument('<action>', 'export or import')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('-t, --target <path>', 'Alias for --directory (backwards compat)')
  .requiredOption('--session <id>', 'Duel session or engagement ID')
  .requiredOption('--role <role>', 'red, blue, or referee')
  .requiredOption('--bundle <path>', 'JSON bundle path to write or read')
  .action((action, options) => {
    if (!['export', 'import'].includes(action)) {
      console.error(chalk.red(`\n  Unknown broker action: ${action}`));
      console.error(chalk.gray('  Valid actions: export, import\n'));
      process.exit(1);
    }
    const targetDir = options.directory || options.target;
    const targetRoot = detectProjectRoot(targetDir);
    const script = getExecutionScript(targetRoot, 'red-blue-broker.py');
    const outputRoot = getDuelOutputRoot(targetRoot);
    const args = [
      script,
      action,
      '--session',
      options.session,
      '--role',
      options.role,
      '--output-root',
      outputRoot,
      '--bundle',
      path.resolve(options.bundle),
    ];
    try {
      execFileSync('python3', args, { stdio: 'inherit' });
    } catch (error) {
      process.exit(error.status || 1);
    }
  });

// --- status ----------------------------------------------------------------
program
  .command('status')
  .description('Show SPECTRA installation status')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('-t, --target <path>', 'Alias for --directory (backwards compat)')
  .action(async (options) => {
    console.log(BANNER);

    const targetDir = options.directory || options.target;
    const targetRoot = detectProjectRoot(targetDir);
    const spectraDir = `${targetRoot}/_spectra`;

    const existing = checkExistingInstallation(spectraDir);
    if (!existing.exists) {
      console.error(chalk.red('\n  No SPECTRA installation found.'));
      console.error(chalk.gray('  Run: npx spectra-method install\n'));
      process.exit(1);
    }

    const manifest = readManifest(spectraDir);
    if (!manifest) {
      console.error(chalk.red('\n  Manifest file missing or corrupt.'));
      console.error(chalk.gray('  Run: npx spectra-method install --force\n'));
      process.exit(1);
    }

    const inst = manifest.installation || {};
    console.log(chalk.white('\n  Installation'));
    console.log(chalk.gray('  ----------------------------------------'));
    console.log(`  Name:         ${chalk.cyan(inst.name || 'SPECTRA')}`);
    console.log(`  Version:      ${chalk.cyan(inst.version || 'unknown')}`);
    console.log(`  Installed:    ${chalk.gray(inst.installDate || 'unknown')}`);
    console.log(`  Last Updated: ${chalk.gray(inst.lastUpdated || 'unknown')}`);
    console.log(`  Location:     ${chalk.gray(spectraDir)}`);
    console.log(`  Output:       ${chalk.gray(inst.outputFolder || '_spectra-output')}`);
    if (inst.userName) {
      console.log(`  User:         ${chalk.gray(inst.userName)}`);
    }
    if (inst.communicationLanguage) {
      console.log(`  Comm. lang:   ${chalk.gray(inst.communicationLanguage)}`);
    }
    if (inst.documentOutputLanguage) {
      console.log(`  Doc. lang:    ${chalk.gray(inst.documentOutputLanguage)}`);
    }

    console.log(chalk.white('\n  Modules'));
    console.log(chalk.gray('  ----------------------------------------'));
    const modules = manifest.modules || [];
    for (const mod of modules) {
      const info = MODULE_INFO[mod.name] || { icon: '\u2022', name: mod.displayName || mod.name };
      const configStatus = existing.hasConfig?.[mod.name]
        ? chalk.green('configured')
        : chalk.yellow('needs init');
      console.log(`  ${info.icon}  ${chalk.bold(mod.name.toUpperCase().padEnd(6))} v${mod.version}  ${configStatus}  ${chalk.gray(mod.source || 'built-in')}`);
    }

    const ides = manifest.ides || [];
    if (ides.length > 0) {
      console.log(chalk.white('\n  IDE Support'));
      console.log(chalk.gray('  ----------------------------------------'));
      for (const ide of ides) {
        console.log(`  \u2713 ${ide}`);
      }
    }

    // Skill count
    const skillsDir = `${targetRoot}/.claude/skills`;
    if (fs.existsSync(skillsDir)) {
      const skillDirs = fs.readdirSync(skillsDir).filter(d =>
        d.startsWith('spectra-') && fs.statSync(`${skillsDir}/${d}`).isDirectory()
      );
      console.log(chalk.white('\n  Skills'));
      console.log(chalk.gray('  ----------------------------------------'));
      console.log(`  ${skillDirs.length} SPECTRA skills registered in .claude/skills/`);
    }
    const codexIndex = `${targetRoot}/.codex/spectra/skill-index.json`;
    if (fs.existsSync(codexIndex)) {
      const codexSkills = JSON.parse(fs.readFileSync(codexIndex, 'utf-8')).skills || [];
      console.log(chalk.white('\n  Codex'));
      console.log(chalk.gray('  ----------------------------------------'));
      console.log(`  ${codexSkills.length} SPECTRA skills indexed in .codex/spectra/`);
      console.log('  AGENTS.md SPECTRA adapter block present');
    }

    console.log();
  });

// --- update ----------------------------------------------------------------
program
  .command('update')
  .description('Update SPECTRA to latest version')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('-t, --target <path>', 'Alias for --directory (backwards compat)')
  .option('--tools <tools>', 'Comma-separated IDE IDs (e.g., "claude-code,codex"). Use "none" to skip.', 'claude-code')
  .action(async (options) => {
    console.log(BANNER);

    const targetDir = options.directory || options.target;
    const targetRoot = detectProjectRoot(targetDir);
    const spectraDir = `${targetRoot}/_spectra`;

    const existing = checkExistingInstallation(spectraDir);
    if (!existing.exists) {
      console.error(chalk.red('\n  No SPECTRA installation found. Use install instead.'));
      console.error(chalk.gray('  Run: npx spectra-method install\n'));
      process.exit(1);
    }

    const currentVersion = existing.version || '0.0.0';
    const latestVersion = getPackageVersion();

    console.log(chalk.white('\n  Current version: ') + chalk.gray(currentVersion));
    console.log(chalk.white('  Package version: ') + chalk.cyan(latestVersion));
    console.log();

    if (currentVersion === latestVersion) {
      console.log(chalk.green('  Already up to date.\n'));
      return;
    }

    // Read current manifest to know which modules are installed
    const manifest = readManifest(spectraDir);
    const installedModules = manifest?.modules?.map(m => m.name) || ALL_MODULES;

    // Parse --tools
    const toolsList = options.tools === 'none'
      ? []
      : options.tools.split(',').map(t => t.trim().toLowerCase());
    const invalidIdes = toolsList.filter(t => !SUPPORTED_IDES.includes(t));
    if (invalidIdes.length > 0) {
      console.error(chalk.red(`\n  Unknown IDE(s): ${invalidIdes.join(', ')}`));
      console.error(chalk.gray(`  Supported IDEs: ${SUPPORTED_IDES.join(', ')}, or "none" to skip`));
      process.exit(1);
    }

    // Step 1: Backup configs
    console.log(chalk.gray('  [1/4] Backing up user configurations...'));
    const savedConfigs = preserveUserConfigs(spectraDir);
    console.log(chalk.green(`  \u2713 Backed up ${savedConfigs.count} config file(s)`));

    // Step 2: Copy updated framework files
    console.log(chalk.gray('  [2/4] Updating framework files...'));
    const sourcePath = getSourcePath();
    const copyResult = copyFrameworkFiles(sourcePath, spectraDir, {
      modules: installedModules,
    });
    console.log(chalk.green(`  \u2713 Updated ${copyResult.fileCount} files`));

    // Step 3: Restore configs and update manifest
    console.log(chalk.gray('  [3/4] Restoring configurations...'));
    restoreUserConfigs(spectraDir, savedConfigs);

    // Re-register skills
    if (toolsList.length > 0) {
      for (const ide of toolsList) {
        const skillResult = registerSkillsForIDE(targetRoot, ide, {
          modules: installedModules,
          spectraDir,
        });
        console.log(chalk.green(`  \u2713 Re-registered ${skillResult.registered} skills for ${ide}`));
      }
    }

    writeManifest(spectraDir, {
      version: latestVersion,
      modules: installedModules,
      ides: toolsList,
      previousVersion: currentVersion,
      outputFolder: manifest?.installation?.outputFolder || '_spectra-output',
      userName: manifest?.installation?.userName,
      communicationLanguage: manifest?.installation?.communicationLanguage,
      documentOutputLanguage: manifest?.installation?.documentOutputLanguage,
    });
    console.log(chalk.green('  \u2713 Configuration restored'));

    // Step 4: Verify
    console.log(chalk.gray('  [4/4] Verifying...'));
    const initResult = runInitCheck(spectraDir);
    if (!initResult.success) {
      console.log(chalk.yellow(`\n  \u26A0 Post-update check: ${initResult.message}`));
    } else {
      console.log(chalk.green('  \u2713 Installation verified'));
    }

    console.log(chalk.green.bold(`\n  SPECTRA updated: ${currentVersion} -> ${latestVersion}\n`));
  });

// ---------------------------------------------------------------------------
// Parse and run
// ---------------------------------------------------------------------------
program.parse();
