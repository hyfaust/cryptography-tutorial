// 自定义 JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // 为命令行输出添加提示符样式
    document.querySelectorAll('code.language-console').forEach(function (block) {
        block.innerHTML = block.innerHTML.replace(/^(\$ )/gm, '<span class="prompt">$ </span>');
    });
});
