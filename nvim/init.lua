-- Ensure Homebrew binaries are in PATH on macOS (essential for tree-sitter CLI and compilers)
if vim.fn.has("mac") == 1 then
    vim.env.PATH = "/opt/homebrew/bin:" .. vim.env.PATH
end

--    ui2 provides resedign & rewrite of nvim's message routing & 
--    command line system
require("vim._core.ui2").enable({})

require("options")
require("keymaps")
require("commands")
require("pack")

vim.cmd.colorscheme("alduin")
-- vim.opt.background = "dark"
-- vim.cmd.colorscheme("gruvbox")
vim.opt.cmdheight = 0
