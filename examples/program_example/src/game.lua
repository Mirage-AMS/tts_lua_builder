require("mock/default")
require("com/const")
require("com/basic")
require("src/build_data")

local function clearScriptingZones()
    local objTbl = self.getObjects()
    for _, obj in ipairs(objTbl) do
        if isScripting(obj) then
            obj.destruct()
        end
    end
end

function FactoryCreateGame()
    local game = {
        version = 0,
    }
    ---------------------------------------------------------------------
    --  Save and Load
    ---------------------------------------------------------------------
    function game:onLoad(savedData)
        local data
        if savedData and savedData ~= "" then
            print("Parsing saved data")
            local loadedData = JSON.decode(savedData)

            -- Validate data version
            if loadedData and tonumber(loadedData.version) then
                local dataVersion = tonumber(loadedData.version)
                local currentVersion = tonumber(SCRIPT_VERSION)

                if dataVersion >= currentVersion then
                    print("Using saved data")
                    data = loadedData
                else
                    print("Saved data version is too old, using default data")
                    data = buildDefaultData()
                    clearScriptingZones()
                end
            else
                print("Saved data format is invalid, using default data")
                data = buildDefaultData()
                clearScriptingZones()
            end
        else
            print("No saved data, using default data")
            data = buildDefaultData()
            clearScriptingZones()
        end

        -- Update Game version
        self.version = SCRIPT_VERSION

        -- initialize Game
        self:init()

        return self
    end

    function game:onSave()
        local savedData = {
            version = self.version,
        }
        return JSON.encode(savedData)
    end

    function game:init()
        print("Init Game")
    end

    return game
end