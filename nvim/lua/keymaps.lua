vim.g.mapleader = " "  
vim.g.mapleader = " "  

-- replaces selected text w/o losing what was yanked 
vim.keymap.set("x", "p", [["_dP]], { desc = "Paste over selectio w/o losing yanked text" }) 

-- delete text w/o saving to any register 
vim.keymap.set({ "n", "v" }, "<leader>d", [["_d]], { desc = "Delete w/o yanking" })

vim.keymap.set("i", "<C-c>", "<Esc>")
vim.keymap.set("n", "<C-c>", ":nohl<CR>", { desc = "Clear search highlighting", silent = true }) 

vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv", { desc = "moves lines down in visual selection" })
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv", { desc = "moves lines up in  visual selection" })

vim.keymap.set("v", "<", "<gv", { desc = "Unindent and keep selection" }) 
vim.keymap.set("v", ">", ">gv", { desc = "Indent and keep selection" })

vim.keymap.set("n", "J", "mzJ`z", { desc = "Join lines w/o moving cursor" }) 

vim.keymap.set("n", "<C-d>", "<C-d>zz", { desc = "move down in buffer with cursor centered" })
vim.keymap.set("n", "<C-u>", "<C-u>zz", { desc = "move up in buffer with cursor centered"}) 

vim.keymap.set("n", "n", "nzzzv", { desc = "Next search result cursor centered" })
vim.keymap.set("n", "N", "Nzzzv", { desc = "Previous search result cursor centered" })

vim.keymap.set("n", "<leader>re", "<cmd>restart<cr>", { desc = "Restart neovim (:restart)" }) 

-- native undotree 
vim.keymap.set("n", "<leader>u", function() 
    vim.cmd.packadd("nvim.undotree")
    require("undotree").open()
end, { desc = "Toggle builtin undotree" }) 
