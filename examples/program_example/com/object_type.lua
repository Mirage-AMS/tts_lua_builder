require("com/const")

function isDeck(object)
    if object == nil then return false end
    return object.type == TYPE_DECK
end

function isCard(object)
    if object == nil then return false end
    return object.type == TYPE_CARD
end

function isTile(object)
    if object == nil then return false end
    return object.type == TYPE_TILE
end

function isScripting(object)
    if object == nil then return false end
    return object.type == TYPE_SCRIPTING
end

function isCardLike(object)
    return isCard(object) or isDeck(object)
end
