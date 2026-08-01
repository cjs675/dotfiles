  ### 🔑 General & Leader Key

  • Leader Key: <Space> (keymaps.lua)
  ──────
  ### 📦 Custom Package Commands

  *Defined in commands.lua*

   Command                     | Usage                       | Description
  -----------------------------|-----------------------------|--------------------------------------------------------
   :PackAdd                    | :PackAdd user/repo          | Installs / adds new plugin repository via vim.pack
   :PackDel                    | :PackDel plugin_name        | Removes specified plugins
   :PackUpdate                 | :PackUpdate [plugin]        | Updates all plugins (or specific plugins if specified)
  ──────
  ### 🔍 Telescope / Mini.Pick & Navigation

  *Defined in pack.lua*

   Keymap               |        Mode         | Action / Function              | Description
  ----------------------|---------------------|--------------------------------|--------------------------------------
   <leader>pf           |          N          | MiniPick.builtin.files()       | Open file finder picker
   <leader>ps           |          N          | MiniPick.builtin.grep()        | Live grep / word search under cursor
   <leader>vh           |          N          | MiniPick.builtin.help()        | Help tags picker
   <leader>xx           |          N          | MiniExtra.pickers.diagnostic() | Workspace LSP diagnostics picker
   <leader>pk           |          N          | MiniExtra.pickers.keymaps()    | Interactive keymap search picker
  ──────
  ### 📁 File Exploration

  *Defined in pack.lua & pack.lua*

  #### mini.files

   Keymap                   |          Mode           | Description
  --------------------------|-------------------------|---------------------------------------------------------------
   -                        |            N            | Toggle mini.files file explorer
   <leader>-                |            N            | Open mini.files focused & revealed at the current opened file

  Navigation inside mini.files:

  • <CR> or L : Navigate into directory / open file
  • _ or H : Navigate out to parent directory

  #### nvim-tree

   Keymap                              |                Mode                 | Description
  -------------------------------------|-------------------------------------|----------------------------------------
   <leader>e                           |                  N                  | Toggle nvim-tree sidebar file explorer
  ──────
  ### 💡 LSP & Diagnostics

  *Defined in lsp.lua*

   Keymap		  |         Mode          | Action                    | Description
  ------------------------|-----------------------|---------------------------|---------------------------------------
   gd                     |           N           | vim.lsp.buf.definition    | Jump to definition under cursor
   <leader>f		  |           N           | vim.lsp.buf.format        | Format current buffer
   <leader>df		  |           N           | vim.diagnostic.open_float | Show line diagnostics floating window

  Configured Language Servers: lua_ls, clangd, gopls, ts_ls. Managed via Mason (:Mason).
  ──────
  ### ✂️ Text Editing, Registers & Motion

  *Defined in keymaps.lua & init.lua*

   Keymap           |       Mode       | Description
  ------------------|------------------|------------------------------------------------------------------------------
   p                |        V         | Paste over visual selection without overwriting default yank register ("_dP)
   <leader>d        |       N, V       | Delete text without saving to yank register ("_d)
   <C-c>            |        I         | Map <C-c> to <Esc>
   <C-c>            |        N         | Clear search highlight (:nohl)
   J                |        N         | Join lower line without moving cursor position (mzJz`)
   J / K            |        V         | Move selected lines down / up and re-indent (:m '>+1, :m '<-2)
   < / >            |        V         | Unindent / indent selection while maintaining visual selection
   <C-d> / <C-u>    |        N         | Scroll half-page down / up with cursor auto-centered (zz)
   n / N            |        N         | Jump to next / previous search result centered (zzzv)
   ```              |      I (md)      | Auto-closes Markdown codeblock and places cursor inside
  ──────
  ### 🛠️ Mini Modules & Builtins

  #### mini.surround (Surrounding text object controls)

  *Defined in pack.lua*

   Key Combo                                                | Action
  ----------------------------------------------------------|---------------------------------------------------------
   sa                                                       | Add surrounding
   sd                                                       | Delete surrounding
   sr                                                       | Replace surrounding
   sf / sF                                                  | Find surrounding (right / left)
   sh                                                       | Highlight surrounding
   sn                                                       | Update n_lines

  #### Git Integration (mini.diff & vim-fugitive)

  *Defined in pack.lua*

   Keymap              |        Mode         | Description
  ---------------------|---------------------|------------------------------------------------------------------------
   <leader>gg          |          N          | Open Fugitive Git status full page in a new tab (:tabnew | Git | only)
   <leader>gd          |          N          | Open Git diff split for active buffer (:Gvdiffsplit)

  #### Undo Tree & System

  *Defined in keymaps.lua*

   Keymap			|            Mode             | Description
  ------------------------------|-----------------------------|-------------------------------------------------------
   <leader>u			|              N              | Toggle Neovim native Undo Tree viewer (nvim.undotree)
   <leader>re			|              N              | Restart Neovim (:restart)
  ──────
  ### 🚀 Dashboard Quick Keys

  *Defined in pack.lua*

  When opening Neovim without a file, press:

  • c — Open configuration file (pack.lua)
  • f — Find files (mini.pick)
  • s — Word search (mini.pick)
  • q — Quit Neovim (:qa)
