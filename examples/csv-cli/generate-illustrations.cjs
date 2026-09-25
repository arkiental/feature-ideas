// Original, editable concept diagrams. Node.js 18+; no dependency for SVG output.
// Optional PNG rendering: install sharp, then node generate-illustrations.cjs --png
const fs = require('node:fs');
const path = require('node:path');
const out = path.join(__dirname, 'images');
fs.mkdirSync(out, { recursive: true });
const esc = s => String(s).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const text = (x,y,s,size=22,color='#142D3A',extra='') => `<text x="${x}" y="${y}" font-family="Arial, sans-serif" font-size="${size}" fill="${color}" ${extra}>${esc(s)}</text>`;
const mono = (x,y,s,color='#E7F0EE',size=21) => `<text x="${x}" y="${y}" xml:space="preserve" font-family="Consolas, monospace" font-size="${size}" fill="${color}">${esc(s)}</text>`;
const items = [
 {id:'01-schema-validation', title:'Catch invalid data before it moves', sub:'01 · Schema validation · Tablecraft concept', cmd:['$ tablecraft validate orders.csv', '    --schema orders.schema.json'], lines:['Rules: qty = integer >= 1', '       price = decimal >= 0', '', 'Row 3  qty    -2   must be >= 1', 'Row 4  price  USD  expected decimal', '', '4 rows checked · 2 invalid · exit 1'], notes:[['Declare the contract', 'Version a local schema file.', 'Reuse the same rules in CI.'],['Find the failing field', 'Show row, column, and reason.', 'Cap error output by default.'],['Keep the source intact', 'Validation reads only.', 'An invalid row returns exit 1.']], result:'Outcome: a reproducible pass/fail gate, with actionable diagnostics.'},
 {id:'02-transform-preview', title:'See a transformation before saving it', sub:'02 · Dry-run preview · Tablecraft concept', cmd:['$ tablecraft derive orders.csv', '    total="price * qty" --preview 5'], lines:['INPUT                   PROPOSED', 'sku    price   qty       total', 'A-104  12.50    2         25.00', 'B-208   8.00    3         24.00', '', '2 of 2 rows previewed', 'No output file written'], notes:[['Use the same evaluator', 'Preview and derive share', 'expression and decimal rules.'],['Compare the result', 'Align source and new values.', 'Limit the sample to 5 rows.'],['Save with an explicit path', 'Remove --preview and add', '--output enriched.csv.']], result:'Outcome: check a bounded sample before running the full transform.'},
 {id:'03-saved-recipes', title:'Repeat a workflow without rebuilding it', sub:'03 · Saved recipes · Tablecraft concept', cmd:['$ tablecraft run monthly.json', '    --input orders.csv', '    --output report.csv'], lines:['recipeVersion: 1', '1  validate  orders.schema.json', '2  derive    total = price * qty', '3  select    sku, qty, total', '', 'Source unchanged', 'Report written: report.csv'], notes:[['Commit the workflow', 'Store an ordered recipe', 'with a versioned format.'],['Validate before execution', 'Check every step and path.', 'Reject unknown operations.'],['Publish after success', 'Use a temporary output.', 'Keep an existing file intact.']], result:'Outcome: teammates run the same declared steps with new input files.'},
 {id:'04-streaming-profile', title:'Understand a large file in one pass', sub:'04 · Streaming profile · Tablecraft concept', cmd:['$ tablecraft profile events.csv', '    --max-categories 100'], lines:['ROWS        1,200,000', 'account_id  missing: 24', 'amount      numeric: 1,199,980', '            invalid: 20', 'region      tracked: 100 values', '            overflow: yes', '', 'Counts exact · no distinct estimate'], notes:[['Bound the memory', 'Read records one at a time.', 'Keep capped per-column state.'],['Expose uncertainty', 'Track at most 100 categories.', 'Report overflow explicitly.'],['Keep the report usable', 'Send progress to stderr.', 'Emit text or JSON to stdout.']], result:'Outcome: spot missing and malformed values without loading all rows.'},
 {id:'05-safe-quarantine', title:'Separate bad rows without losing them', sub:'05 · Safe quarantine · Tablecraft concept', cmd:['$ tablecraft validate orders.csv', '    --schema orders.schema.json', '    --quarantine-dir review-001'], lines:['review-001/', '  accepted.csv    988 records', '  rejected.csv     12 records', '  errors.jsonl     12 diagnoses', '  manifest.json   status: complete', '', '1,000 = 988 + 12 · exit 1'], notes:[['Reuse the schema rules', 'Send each parsed record', 'to exactly one output.'],['Preserve repair context', 'Retain rejected field values.', 'Link errors by record index.'],['Publish one complete run', 'Stage in the same filesystem.', 'Refuse an existing directory.']], result:'Outcome: continue with valid records and retain a clear repair queue.'}
];
async function main() {
  for (const item of items) {
    let s = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760" role="img" aria-labelledby="title desc"><title id="title">${esc(item.title)}</title><desc id="desc">${esc(item.sub)}. Fictional commands and illustrative output. ${esc(item.result)}</desc><rect width="1200" height="760" fill="#F6F4EB"/>`;
    s += text(48,48,item.sub,19,'#346354','font-weight="700"');
    s += text(48,99,item.title,36,'#142D3A','font-weight="700"');
    s += text(48,133,'Fictional specification walkthrough · not a terminal capture',18,'#53686D');
    s += '<rect x="48" y="170" width="672" height="415" rx="14" fill="#142D3A"/>';
    s += text(72,204,'PROPOSED COMMAND + ILLUSTRATIVE OUTPUT',14,'#ABCBC0','letter-spacing="1.3"');
    item.cmd.forEach((l,i)=>s+=mono(72,244+i*28,l,'#A8E8C4',20));
    const start=244+item.cmd.length*28+25;
    item.lines.forEach((l,i)=>s+=mono(72,start+i*28,l));
    item.notes.forEach((n,i)=>{
      const y=170+i*140;
      s += `<rect x="748" y="${y}" width="404" height="126" rx="10" fill="#E7ECE1"/><circle cx="778" cy="${y+30}" r="15" fill="#24674F"/>`;
      s += text(778,y+36,i+1,17,'#FFFFFF','text-anchor="middle" font-weight="700"');
      s += text(806,y+37,n[0],22,'#142D3A','font-weight="700"');
      s += text(774,y+72,n[1],21);
      s += text(774,y+102,n[2],21);
    });
    s += '<rect x="48" y="618" width="1104" height="77" rx="10" fill="#D6E8D8"/>';
    s += text(72,664,item.result,23,'#174B38','font-weight="700"');
    s += text(48,732,'FEATURE IDEAS / TABLECRAFT',14,'#53686D','letter-spacing="1.5"');
    s += text(1152,732,'CONCEPT · SYNTHETIC DATA',14,'#53686D','text-anchor="end" letter-spacing="1.2"');
    s += '</svg>';
    fs.writeFileSync(path.join(out, item.id+'.svg'),s+'\n');
    if(process.argv.includes('--png')) { const sharp=require('sharp'); await sharp(Buffer.from(s)).png().toFile(path.join(out,item.id+'.png')); }
  }
}
main().catch(e=>{ console.error(e); process.exitCode=1; });
