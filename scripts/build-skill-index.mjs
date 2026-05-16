#!/usr/bin/env node
/**
 * Build compact skill index from _config/skill-manifest.csv.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const repoRoot = path.resolve(path.dirname(__filename), '..');
const input = path.join(repoRoot, '_config', 'skill-manifest.csv');
const output = path.join(repoRoot, '_config', 'skill-index.json');

function parseCSVLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && i + 1 < line.length && line[i + 1] === '"') {
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

const content = fs.readFileSync(input, 'utf-8').trim();
const lines = content.split('\n');
const header = parseCSVLine(lines[0]);
const idx = {
  id: header.indexOf('canonicalId'),
  name: header.indexOf('name'),
  desc: header.indexOf('description'),
  module: header.indexOf('module'),
  path: header.indexOf('path'),
  install: header.indexOf('install_to_spectra'),
};

const skills = lines.slice(1)
  .map(line => parseCSVLine(line))
  .filter(cols => cols[idx.id])
  .map(cols => ({
    id: cols[idx.id],
    n: cols[idx.name],
    d: cols[idx.desc],
    m: cols[idx.module],
    p: cols[idx.path],
    i: (cols[idx.install] || '').toLowerCase() === 'true',
  }));

const moduleCounts = skills.reduce((acc, skill) => {
  acc[skill.m] = (acc[skill.m] || 0) + 1;
  return acc;
}, {});

const index = {
  version: 1,
  generated_from: '_config/skill-manifest.csv',
  count: skills.length,
  module_counts: moduleCounts,
  skills,
};

fs.writeFileSync(output, `${JSON.stringify(index, null, 2)}\n`, 'utf-8');
console.log(`Built ${path.relative(repoRoot, output)} with ${skills.length} skills.`);
