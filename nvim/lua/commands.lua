vim.api.nvim_create_user_command("PackAdd", function(opts)
    vim.pack.add(opts.fargs)
end, { nargs = "+", desc = "Add plugins (:PackAdd user/repo user/repo2)" }) 

vim.api.nvim_create_user_command("PackDel", function(opts)
    vim.pack.del(opts.fargs)
end, { nargs = "+", desc = "Delete plugins (:PackDel plugin1 plugin2)" })

vim.api.nvim_create_user_command("PackUpdate", function(opts)
    -- check if any arg is passed 
    if opts.args:match("%S") then
        -- update specific plugins 
        local plugins = vim.split(opts.args, "%s+", { trimempty = true })
        -- update only specified plugins 
        vim.pack.update(plugins)
    else 
        -- update all
        vim.pack.update() 
    end
end, { nargs = "*", desc = "Update all plugins or specified ones" }) 
