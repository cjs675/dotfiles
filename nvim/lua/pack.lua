vim.pack.add({
    "https://github.com/AlessandroYorba/Alduin",
    "https://github.com/nvim-mini/mini.nvim",
    "https://github.com/rafamadriz/friendly-snippets",
    { src = "https://github.com/nvim-treesitter/nvim-treesitter", branch = "master" },
    "https://github.com/neovim/nvim-lspconfig",
    "https://github.com/mason-org/mason.nvim",
    "https://github.com/tpope/vim-fugitive",
    "https://github.com/nvim-tree/nvim-web-devicons",
    "https://github.com/nvimdev/dashboard-nvim",
    "https://github.com/ellisonleao/gruvbox.nvim",
    "https://github.com/nvim-tree/nvim-tree.lua",
    "https://github.com/saghen/blink.cmp",
    "https://github.com/saghen/blink.lib",
    "https://github.com/nvim-telescope/telescope.nvim",
    "https://github.com/stevearc/conform.nvim",
    "https://github.com/akinsho/toggleterm.nvim",

})

-- mini files --
local MiniFiles = require("mini.files")
MiniFiles.setup({
    mappings = {
        go_in = "<CR>",
        go_in_plus = "L",
        go_out = "_",
        go_out_plus = "H",
    }
})

vim.keymap.set("n", "-", "<cmd>lua MiniFiles.open()<CR>", { desc = "Toggle mini file explorer" })
vim.keymap.set("n", "<leader>-", function()
    MiniFiles.open(vim.api.nvim_buf_get_name(0), false)
    MiniFiles.reveal_cwd()
end, { desc = "Toggle into currently opened file" })

-- mini notify --
local MiniNotify = require("mini.notify")
require("mini.notify").setup({
    -- only show messages
    content = {
        format = function(notif)
            return notif.msg
        end,
    }
})

-- mini pairs (auto close brackets) --
require("mini.pairs").setup()

-- mini cmdline completion --
require("mini.cmdline").setup({
    autocorrect = { enable = false }
})

-- mini surround --
require("mini.surround").setup()
-- Default Keymaps --
-- | 'sa' | Add surrounding             |
-- | 'sd' | Delete surrounding          |
-- | 'sr' | Replace surrounding         |
-- | 'sf' | Find surrounding (right)    |
-- | 'sF' | Find surrounding (left)     |
-- | 'sh' | Highlight surrounding       |
-- | 'sn' | Update n_lines              |
-- | 'l' / 'n' | as suffix for prev/next|

-- mini picker --
local MiniPick = require("mini.pick")
local MiniExtra = require("mini.extra")

MiniPick.setup()
MiniExtra.setup()

vim.keymap.set("n", "<leader>pf", function() MiniPick.builtin.files() end, { desc = "Mini File Picker" })
vim.keymap.set("n", "<leader>ps", function() MiniPick.builtin.grep({ pattern = vim.fn.expand("<cword>") }) end,
    { desc = "Word search" })
vim.keymap.set("n", "<leader>vh", function() MiniPick.builtin.help() end, { desc = "Mini Help" })

vim.keymap.set("n", "<leader>xx", function() MiniExtra.pickers.diagnostic() end, { desc = "Mini picker diagnostics" })
vim.keymap.set('n', '<leader>pk', function() MiniExtra.pickers.keymaps() end, { desc = 'Search keymaps' })

-- mini completions --
require("mini.completion").setup({
    lsp_completion = {
        auto_setup = true,
    }
})

-- mini snippets --
local MiniSnippets = require("mini.snippets")
MiniSnippets.setup({
    snippets = {
        MiniSnippets.gen_loader.from_lang(), -- loads friendly snippets automatically
    },
    -- disable empty tabstop indicators
    expand = {
        insert = function(snippet)
            MiniSnippets.default_insert(snippet, { empty_tabstop = "" })
        end,
    },
})
MiniSnippets.start_lsp_server({ match = false })

vim.api.nvim_create_autocmd("Colorscheme", {
    callback = function()
        vim.api.nvim_set_hl(0, "MiniSnippetsCurrent", {})
        vim.api.nvim_set_hl(0, "MiniSnippetsCurrentReplace", {})
        vim.api.nvim_set_hl(0, "MiniSnippetsFinal", {})
        vim.api.nvim_set_hl(0, "MiniSnippetsUnvisited", {})
        vim.api.nvim_set_hl(0, "MiniSnippetsVisited", {})
    end,
})
-- support for git & fugitive) --
local MiniDiff = require("mini.diff")
MiniDiff.setup({
    source = MiniDiff.gen_source.git({ index = false }),
})

vim.keymap.set("n", "<leader>gg", "<cmd>tabnew | Git | only<cr>", { desc = "Fugitive Full Page New Tab" })
vim.keymap.set("n", "<leader>gd", "<cmd>Gvdiffsplit<CR>", { desc = "Git diff split", })


-- nvim treesitter --
require("treesitter")

-- nvim-web-devicons --
require("nvim-web-devicons").setup()

-- lsp --
require("lsp")

-- mini statusline
require("mini.statusline").setup({
    use_icons = true,
    set_vim_settings = false,
})

-- initialize maston to manage external tooling libs 
require("mason").setup()

-- nvim-tree setup --
require("nvim-tree").setup({
    view = {
        width = 30,
        side = "left",
    },
    filters = {
        dotfiles = true,
    },
})
vim.keymap.set("n", "<leader>e", "<cmd>NvimTreeToggle<CR>", { desc = "Toggle Sidebar File Tree" })


-- grab nvim's default capabilities
local default_caps = vim.lsp.protocol.make_client_capabilities()

-- add clangd-specific encoding to fix defaults 
default_caps.offsetEncoding = { "utf-16" }

-- configure c++ lang server (clangd) 
vim.lsp.config('clangd', {
    cmd = {
        "clangd",
        "--background-index",
        "--clang-tidy",
        "--header-insertion=iwyu",
        "--completion-style=detailed",
    },
    -- fix common conflict between clangd & encoding preferences 
    capabilities =  default_caps,
})

vim.lsp.enable('clangd')



-- dashboard.vim --
require("dashboard").setup({
    theme = 'hyper',
    config = {
        header = {
            [[     ▀████▀▄▄              ▄█]],
            [[            █▀    ▀▀▄▄▄▄▄    ▄▄▀▀█ ]],
            [[    ▄        █          ▀▀▀▀▄  ▄▀  ]],
            [[   ▄▀ ▀▄      ▀▄              ▀▄▀  ]],
            [[  ▄▀    █     █▀   ▄█▀▄      ▄█    ]],
            [[  ▀▄     ▀▄  █     ▀██▀     ██▄█   ]],
            [[   ▀▄    ▄▀ █   ▄██▄   ▄  ▄  ▀▀ █  ]],
            [[    █  ▄▀  █    ▀██▀    ▀▀ ▀▀  ▄▀  ]],
            [[   █   █  █      ▄▄           ▄▀   ]],
            [[                                   ]],
            [[                                   ]],
        },
        shortcut = {
            -- center = {
            {
                icon = ' ',
                icon_hl = '@variable',
                desc = 'Open Config',
                group = 'Label',
                action = 'edit ~/.config/nvim/lua/pack.lua',
                key = 'c',
            },
            {
                icon = ' ',
                icon_hl = '@variable',
                desc = 'Find Files',
                group = 'Label',
                action = 'lua require("mini.pick").builtin.files()',
                key = 'f',
            },
            {
                icon = '󰈭 ',
                icon_hl = '@variable',
                desc = 'Word Search',
                group = 'Label',
                action = 'lua require("mini.pick").builtin.grep()',
                key = 's',
            },
            {
                icon = ' ',
                icon_hl = '@variable',
                desc = 'Quit Neovim',
                group = 'Label',
                action = 'qa',
                key = 'q',
            },
        },
    },
})
