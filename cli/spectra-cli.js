#!/usr/bin/env node
/**
 * SPECTRA CLI -- Security Protocol Engineering for Cyber Threat Response & Assessment
 *
 * Usage:
 *   npx spectra-method install                              Install SPECTRA into current project
 *   npx spectra-method install --modules rtk,soc            Install specific modules only
 *   npx spectra-method install -d ./my-proj --tools claude-code -y  Full options
 *   npx spectra-method validate                             Run project validation
 *   npx spectra-method status                               Show installation status
 *   npx spectra-method update                               Update SPECTRA to latest version
 */

import fs from 'node:fs';
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
  core: { icon: '\u26A1', name: 'Core Framework', agents: 2, skills: 10 },
  rtk:  { icon: '\uD83D\uDD34', name: 'Red Team Kit', agents: 6, workflows: 5 },
  soc:  { icon: '\uD83D\uDD35', name: 'Security Operations Center', agents: 6, workflows: 4 },
  irt:  { icon: '\uD83D\uDFE0', name: 'Incident Response Team', agents: 5, workflows: 4 },
  grc:  { icon: '\u26AA', name: 'Governance, Risk & Compliance', agents: 3, workflows: 3 },
};

const SUPPORTED_IDES = ['claude-code', 'cursor'];

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
  .option('--tools <tools>', 'Comma-separated IDE IDs (e.g., "claude-code,cursor"). Use "none" to skip.', 'claude-code')
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
    const requestedModules = options.modules
      ? options.modules.split(',').map(m => m.trim().toLowerCase())
      : ALL_MODULES;

    // Validate module names
    const invalidModules = requestedModules.filter(m => !ALL_MODULES.includes(m));
    if (invalidModules.length > 0) {
      console.error(chalk.red(`\n  Unknown module(s): ${invalidModules.join(', ')}`));
      console.error(chalk.gray(`  Available modules: ${ALL_MODULES.join(', ')}`));
      process.exit(1);
    }

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
        console.log(chalk.green(`  \u2713 ${skillResult.registered} skills registered in .claude/skills/`));
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
    const frameworkFiles = ['SPECTRA.md', 'DEV-GUIDE.md', '_config/manifest.yaml'];
    for (const file of frameworkFiles) {
      if (fs.existsSync(`${spectraDir}/${file}`)) {
        console.log(chalk.green(`  \u2713 ${file}`));
      } else {
        console.log(chalk.red(`  \u2717 ${file} missing`));
        allValid = false;
      }
    }

    // Check skill registration
    const skillsDir = `${targetRoot}/.claude/skills`;
    if (fs.existsSync(skillsDir)) {
      const skillDirs = fs.readdirSync(skillsDir).filter(d =>
        d.startsWith('spectra-') && fs.statSync(`${skillsDir}/${d}`).isDirectory()
      );
      console.log(chalk.green(`  \u2713 ${skillDirs.length} skills registered in .claude/skills/`));
    } else {
      console.log(chalk.yellow('  \u26A0 No .claude/skills/ directory (run install with --tools claude-code)'));
    }

    // Check output directory
    const outputDir = manifest?.installation?.outputFolder || '_spectra-output';
    if (fs.existsSync(`${targetRoot}/${outputDir}`)) {
      console.log(chalk.green(`  \u2713 Output directory ${outputDir}/ present`));
    } else {
      console.log(chalk.yellow(`  \u26A0 Output directory ${outputDir}/ missing`));
    }

    console.log();
    if (allValid) {
      console.log(chalk.green.bold('  Validation passed.\n'));
    } else {
      console.log(chalk.yellow.bold('  Validation completed with warnings.\n'));
      console.log(chalk.gray('  Run: npx spectra-method install --force   to repair\n'));
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

    console.log();
  });

// --- update ----------------------------------------------------------------
program
  .command('update')
  .description('Update SPECTRA to latest version')
  .option('-d, --directory <path>', 'Target project directory (default: cwd)')
  .option('-t, --target <path>', 'Alias for --directory (backwards compat)')
  .option('--tools <tools>', 'Comma-separated IDE IDs (e.g., "claude-code,cursor"). Use "none" to skip.', 'claude-code')
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
