require("mock/default")
require("com/const")
require("src/game")

function onLoad(saved_data)
    -- check saved data version and decide to use saved data or not
    GAME = FactoryCreateGame():onLoad(saved_data)
end

function onSave()
    return GAME:onSave()
end