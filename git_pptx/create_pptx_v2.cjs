const pptxgen = require('pptxgenjs');
const html2pptx = require('/Users/yhm/.claude/plugins/cache/anthropic-agent-skills/document-skills/ef740771ac90/skills/pptx/scripts/html2pptx.js');
const path = require('path');
const fs = require('fs');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Claude Code';
    pptx.title = 'Git 使用教程';
    pptx.subject = 'Git 基本用法与高阶用法';

    const slidesDir = path.join(__dirname, 'slides_v2');
    const outputPath = path.join(__dirname, 'Git教程_北大红主题.pptx');

    // 获取所有幻灯片HTML文件并排序
    const slideFiles = fs.readdirSync(slidesDir)
        .filter(f => f.match(/slide\d+\.html$/))
        .sort((a, b) => {
            const numA = parseInt(a.match(/\d+/)[0]);
            const numB = parseInt(b.match(/\d+/)[0]);
            return numA - numB;
        });

    console.log(`找到 ${slideFiles.length} 个幻灯片文件`);

    for (const slideFile of slideFiles) {
        const slidePath = path.join(slidesDir, slideFile);
        console.log(`处理: ${slideFile}`);

        try {
            // html2pptx(htmlFile, pres, options) - 它会自动添加slide
            await html2pptx(slidePath, pptx, {
                width: 720,
                height: 405
            });
        } catch (err) {
            console.error(`处理 ${slideFile} 时出错:`, err.message);
        }
    }

    await pptx.writeFile({ fileName: outputPath });
    console.log(`\n演示文稿已保存到: ${outputPath}`);
}

createPresentation().catch(console.error);
