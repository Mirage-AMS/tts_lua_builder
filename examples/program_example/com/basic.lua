function isValInValList(value, list)
    for _, val in ipairs(list) do if val == value then return true end end
    return false
end

function isObjInObjList(target, list)
    if target == nil then return false end
    local target_id = target.getGUID()
    for _, compare in ipairs(list) do
        local compare_id = compare.getGUID()
        if target_id == compare_id then return true end
    end
    return false
end

function isAnyObjInObjList(target_list, list)
    if target_list == nil or target_list == {} then return false end
    for _, target in ipairs(target_list) do
        if isObjInObjList(target, list) then return true end
    end
    return false
end

function getValIdxInValList(value, list)
    for idx, val in ipairs(list) do if val == value then return idx end end
    return nil
end

function mergeList(l1, l2)
    if not l1 then return l2 end
    if not l2 then return l1 end
    for _, v in ipairs(l2) do
        table.insert(l1, v)
    end
    return l1
end

function tableToString(tbl)
    local seen = {}
    local function _tostring(t)
        if type(t) ~= "table" then
            return tostring(t)
        end
        if seen[t] then
            return "<cycle>"
        end
        seen[t] = true

        local parts = {}
        for k, v in pairs(t) do
            local keyStr = type(k) == "string" and k:match("^[%a_][%a%d_]*$") and k or "[".._tostring(k).."]"
            table.insert(parts, keyStr.."=".._tostring(v))
        end
        return "{"..table.concat(parts, ", ").."}"
    end
    return _tostring(tbl)
end

function deepCopy(orig)
    -- record object to avoid infinite loops
    local copies = {}

    local function _copy(obj)
        if type(obj) ~= 'table' then
            return obj
        end
        if copies[obj] then
            return copies[obj]
        end

        local copy = {}
        copies[obj] = copy

        for k, v in pairs(obj) do
            copy[_copy(k)] = _copy(v)
        end

        setmetatable(copy, _copy(getmetatable(obj)))
        return copy
    end

    return _copy(orig)
end

function mergeTable(dst, src)
    if not dst then
        return src
    end

    if not src then
        return dst
    end

    for k, v in pairs(src) do
        if type(v) == "table" then
            if type(dst[k]) ~= "table" then
                dst[k] = {}
            end
            dst[k] = deepCopy(v)
        else
            dst[k] = v
        end
    end

    return dst
end