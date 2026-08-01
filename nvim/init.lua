-- Ensure Homebrew binaries are in PATH on macOS (essential for tree-sitter CLI and compilers)
if vim.fn.has("mac") == 1 then
    vim.env.PATH = "/opt/homebrew/bin:" .. vim.env.PATH
end

--    ui2 provides resedign & rewrite of nvim's message routing & 
--    command line system 
require("pack")
require("options")
require("keymaps")
require("commands")
require("lsp")
require("treesitter")
require("terminal")

vim.cmd.colorscheme("alduin")
-- vim.opt.background = "dark"
-- vim.cmd.colorscheme("gruvbox")
vim.opt.cmdheight = 0

-- diable auto-commenting on newline
vim.api.nvim_create_autocmd("BufEnter", {
    callback = function()
        vim.opt.formatoptions:remove({"c","r", "o" })
    end,
})

vim.api.nvim_create_autocmd("FileType", {
    pattern = "markdown",
    callback = function(args)
        -- disable agressive c-style indenting in markdown 
        vim.opt_local.smartindent = false
        vim.opt_local.cindent = false
        -- auto close 3 backticks, put cursor at end of top backticks 
        vim.keymap.set('i', '```', '```<CR>```<Esc>ka', {
            buffer = args.buf,
            desc = "Auto-close markdown codeblocks"
        })
    end,
})
