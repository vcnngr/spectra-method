#!/usr/bin/env node
/**
 * SPECTRA install smoke tests.
 *
 * Exercises the user-facing CLI against temporary full and partial installs.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const repoRoot = path.resolve(path.dirname(__filename), '..');
const cli = path.join(repoRoot, 'cli', 'spectra-cli.js');
const validator = path.join(repoRoot, 'core', 'execution', 'validate-spectra.py');

function run(command, args, options = {}) {
  return execFileSync(command, args, {
    cwd: repoRoot,
    stdio: options.stdio || 'inherit',
    env: process.env,
  });
}

function runJson(command, args) {
  const output = run(command, args, { stdio: ['ignore', 'pipe', 'inherit'] });
  return JSON.parse(output.toString('utf-8'));
}

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(`${message}: expected ${expected}, got ${actual}`);
  }
}

function makeTempProject(name) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `${name}-`));
}

function smokeFullInstall() {
  const target = makeTempProject('spectra-full');
  run('node', [cli, 'install', '-d', target, '--tools', 'claude-code', '-y', '--user-name', 'CI']);
  run('node', [cli, 'validate', '-d', target, '--deep']);
  const coreConfig = runJson('python3', [
    path.join(target, '_spectra', 'core', 'spectra-init', 'scripts', 'spectra_init.py'),
    'load',
    '--project-root',
    target,
  ]);
  const rtkConfig = runJson('python3', [
    path.join(target, '_spectra', 'core', 'spectra-init', 'scripts', 'spectra_init.py'),
    'load',
    '--module',
    'rtk',
    '--project-root',
    target,
  ]);
  assertEqual(coreConfig.user_name, 'CI', 'core config user_name');
  assertEqual(rtkConfig.user_name, 'CI', 'rtk config user_name');
  assertEqual(rtkConfig.communication_language, 'English', 'rtk config communication_language');
  fs.rmSync(target, { recursive: true, force: true });
}

function smokePartialInstall() {
  const target = makeTempProject('spectra-rtk');
  run('node', [cli, 'install', '-d', target, '--modules', 'rtk', '--tools', 'claude-code', '-y', '--user-name', 'CI']);
  run('node', [cli, 'validate', '-d', target, '--deep']);
  run('python3', [validator, '--path', target, '--strict', '--summary', '--no-color']);
  fs.rmSync(target, { recursive: true, force: true });
}

smokeFullInstall();
smokePartialInstall();
console.log('SPECTRA smoke install tests passed.');
