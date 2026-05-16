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

function assertExists(filePath, message) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`${message}: missing ${filePath}`);
  }
}

function makeTempProject(name) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `${name}-`));
}

function writeSmokeEngagement(target) {
  const dir = path.join(target, '_spectra-output', 'engagements', 'ENG-SMOKE-001');
  fs.mkdirSync(dir, { recursive: true });
  const today = new Date();
  const start = new Date(today.getTime() - 24 * 60 * 60 * 1000).toISOString().slice(0, 10);
  const end = new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);
  const engagement = path.join(dir, 'engagement.yaml');
  fs.writeFileSync(engagement, `engagement:
  id: ENG-SMOKE-001
  name: Smoke engagement
  type: red-team
  status: active
  authorization:
    client: Example Corp
    authorized_by: CISO
    authorization_document: sow.pdf
    start_date: ${start}
    end_date: ${end}
    timezone: UTC
  rules_of_engagement:
    testing_hours: any
    custom_hours: ""
    notify_before_exploit: false
    notify_on_critical: true
    social_engineering_allowed: false
    physical_access_allowed: false
    dos_testing_allowed: false
    data_exfiltration_allowed: false
    production_systems: false
    max_impact_level: high
  scope:
    in_scope:
      networks: []
      domains: [example.com]
      applications: []
      cloud_accounts: []
      users: []
      notes: ""
    out_of_scope:
      networks: []
      domains: [blocked.example.com]
      applications: []
      critical_systems: []
      users: []
      notes: ""
workflow_state: {}
kill_chain: {}
`, 'utf-8');
  return engagement;
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
  assertExists(path.join(target, '_spectra', '_config', 'skill-index.json'), 'compact skill index');
  assertExists(path.join(target, '_spectra', 'core', 'schemas', 'engagement.schema.json'), 'JSON schema');
  assertExists(path.join(target, '_spectra', 'core', 'schemas', 'engagement.schema.yaml'), 'YAML schema');
  assertExists(path.join(target, '_spectra', 'core', 'execution', 'engagement-state.py'), 'engagement state script');
  assertExists(path.join(target, '_spectra', 'core', 'execution', 'report-generator.py'), 'report generator script');
  assertExists(path.join(target, '_spectra', 'core', 'execution', 'party-orchestrator.py'), 'party orchestrator script');
  assertExists(path.join(target, '_spectra', 'core', 'execution', 'duel-orchestrator.py'), 'duel orchestrator script');
  assertExists(path.join(target, '_spectra', 'core', 'execution', 'blue-live-adapter.py'), 'blue live adapter script');
  assertExists(path.join(target, '_spectra', 'core', 'execution', 'red-blue-broker.py'), 'red blue broker script');
  const engagement = writeSmokeEngagement(target);
  run('node', [cli, 'engagement', 'validate', '-d', target, '-e', engagement, '--strict']);
  run('node', [cli, 'engagement', 'gate', '-d', target, '-e', engagement, '--workflow', 'spectra-external-recon', '--target-name', 'example.com']);
  run('node', [cli, 'engagement', 'transition', '-d', target, '-e', engagement, '--workflow', 'spectra-external-recon', '--to', 'in-progress', '--agent', 'CI']);
  const reportPath = path.join(target, '_spectra-output', 'reports', 'ENG-SMOKE-001', 'pentest-report.md');
  run('node', [cli, 'report', 'generate', '-d', target, '-e', engagement, '--type', 'pentest', '--output', reportPath]);
  assertExists(reportPath, 'structured report');
  const partyPath = path.join(target, '_spectra-output', 'party', 'party-plan.json');
  run('node', [cli, 'party', 'plan', '-d', target, '--topic', 'lateral movement detection gap review', '--output', partyPath]);
  assertExists(partyPath, 'party plan');
  run('node', [cli, 'duel', 'init', '-d', target, '--session', 'ENG-SMOKE-001', '--role', 'red', '-e', engagement]);
  run('node', [cli, 'duel', 'init', '-d', target, '--session', 'ENG-SMOKE-001', '--role', 'blue', '-e', engagement]);
  run('node', [cli, 'duel', 'record', '-d', target, '--session', 'ENG-SMOKE-001', '--role', 'red', '--event-type', 'action', '--summary', 'Low-and-slow auth test within noise budget.', '--target-name', 'example.com', '--technique', 'T1110.001']);
  run('node', [cli, 'duel', 'record', '-d', target, '--session', 'ENG-SMOKE-001', '--role', 'blue', '--event-type', 'detection', '--summary', 'Detected auth failures in telemetry.', '--target-name', 'example.com', '--technique', 'T1110.001', '--red-event-id', 'RED-0001']);
  const authLog = path.join(target, '_spectra-output', 'duel', 'smoke-auth.log');
  fs.writeFileSync(authLog, 'May 16 10:00:00 host sshd[100]: Failed password for invalid user admin from 203.0.113.10 port 53222 ssh2\n', 'utf-8');
  run('node', [cli, 'blue', 'ingest', '-d', target, '--session', 'ENG-SMOKE-001', '--source', `auth=${authLog}`]);
  const tailLog = path.join(target, '_spectra-output', 'duel', 'smoke-tail-auth.log');
  fs.writeFileSync(tailLog, 'May 16 10:01:00 host sshd[101]: Failed password for invalid user test from 203.0.113.11 port 53223 ssh2\n', 'utf-8');
  run('node', [cli, 'blue', 'tail', '-d', target, '--session', 'ENG-SMOKE-001', '--source', `auth=${tailLog}`, '--once']);
  fs.appendFileSync(tailLog, 'May 16 10:02:00 host sshd[102]: Failed password for invalid user deploy from 203.0.113.12 port 53224 ssh2\n', 'utf-8');
  run('node', [cli, 'blue', 'tail', '-d', target, '--session', 'ENG-SMOKE-001', '--source', `auth=${tailLog}`, '--once']);
  assertExists(path.join(target, '_spectra-output', 'duel', 'ENG-SMOKE-001', 'blue', 'blue-tail.checkpoint.json'), 'blue tail checkpoint');
  const scorePath = path.join(target, '_spectra-output', 'duel', 'ENG-SMOKE-001', 'scorecard.md');
  run('node', [cli, 'duel', 'score', '-d', target, '--session', 'ENG-SMOKE-001', '--output', scorePath]);
  assertExists(scorePath, 'duel scorecard');
  const redBundle = path.join(target, '_spectra-output', 'duel', 'ENG-SMOKE-001', 'exchange', 'red-bundle.json');
  run('node', [cli, 'broker', 'export', '-d', target, '--session', 'ENG-SMOKE-001', '--role', 'red', '--bundle', redBundle]);
  assertExists(redBundle, 'red broker bundle');
  run('node', [cli, 'broker', 'import', '-d', target, '--session', 'ENG-SMOKE-001', '--role', 'red', '--bundle', redBundle]);
  fs.rmSync(target, { recursive: true, force: true });
}

function smokePartialInstall() {
  const target = makeTempProject('spectra-rtk');
  run('node', [cli, 'install', '-d', target, '--modules', 'rtk', '--tools', 'claude-code', '-y', '--user-name', 'CI']);
  run('node', [cli, 'validate', '-d', target, '--deep']);
  run('python3', [validator, '--path', target, '--strict', '--summary', '--no-color']);
  fs.rmSync(target, { recursive: true, force: true });
}

function smokeLazyModuleAdd() {
  const target = makeTempProject('spectra-lazy');
  run('node', [cli, 'install', '-d', target, '--lazy', '--tools', 'claude-code', '-y', '--user-name', 'CI']);
  run('node', [cli, 'modules', 'list', '-d', target]);
  run('node', [cli, 'modules', 'add', 'rtk', '-d', target, '--tools', 'claude-code']);
  run('node', [cli, 'validate', '-d', target, '--deep']);
  assertExists(path.join(target, '_spectra', 'rtk', 'config.yaml'), 'lazy-loaded RTK config');
  fs.rmSync(target, { recursive: true, force: true });
}

smokeFullInstall();
smokePartialInstall();
smokeLazyModuleAdd();
console.log('SPECTRA smoke install tests passed.');
