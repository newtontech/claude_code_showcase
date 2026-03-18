const pptxgen = require('pptxgenjs');
const html2pptx = require('/Users/yhm/.claude/plugins/cache/anthropic-agent-skills/document-skills/ef740771ac90/skills/pptx/scripts/html2pptx.js');
const path = require('path');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Claude Code';
    pptx.title = 'Git 基础用法';
    pptx.subject = '版本控制入门指南';

    const slidesDir = path.join(__dirname, 'slides');
    const slideFiles = [
        'slide1.html', 'slide2.html', 'slide3.html', 'slide4.html',
        'slide5.html', 'slide6.html', 'slide7.html', 'slide8.html'
    ];

    for (const file of slideFiles) {
        const htmlPath = path.join(slidesDir, file);
        console.log(`Processing: ${file}`);
        await html2pptx(htmlPath, pptx);
    }

    const outputPath = path.join(__dirname, 'git_basics.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`Presentation created: ${outputPath}`);
}

createPresentation().catch(console.error);
