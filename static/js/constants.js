ERRCODES = {
    //GOAL CODES
    CODE_BAD_TITLE: -101,
    CODE_BAD_DESCRIPTION: -102,

    CODE_BAD_PRIZE : -103,
    CODE_GOAL_DNE : -104,
    CODE_BAD_AUTH : -105,
    CODE_BAD_EDIT : -106,
    CODE_BAD_TYPE : -107,
    CODE_BAD_DEADLINE : -108,
    CODE_BAD_ENDING_VALUE : -109,
    CODE_BAD_ENDING_UNIT : -110,
    CODE_GOAL_ENDED : -111,
    CODE_BAD_PRIZE_WITH_VENMO : -112,
    CODE_NOT_AUTHORIZED_WITH_VENMO : -113,

    //USERNAME CODES
    CODE_BAD_USERNAME : -201,           
    CODE_BAD_EMAIL : -202,         
    CODE_BAD_PASSWORD : -203,              
    CODE_FAIL_PASSWORD_CONFIRM : -204, 
    CODE_BAD_CREDENTIAL : -205,    
    CODE_BAD_USERID : -206,
    CODE_NOT_PARTICIPANT : -207,
    CODE_DUPLICATE_USERNAME : -208,
    CODE_DUPLICATE_EMAIL : -209,
    CODE_NOT_FAVORITE : -210,

    //LOG CONSTANTS"
    CODE_BAD_LOG : -301,
    CODE_BAD_AMOUNT : -302,
}

COLORS = {};

COLORS.names = {
    black: "#000000",
    blue: "#0000ff",
    brown: "#a52a2a",
    darkblue: "#00008b",
    darkcyan: "#008b8b",
    darkgrey: "#a9a9a9",
    darkgreen: "#006400",
    darkkhaki: "#bdb76b",
    darkmagenta: "#8b008b",
    darkolivegreen: "#556b2f",
    darkorange: "#ff8c00",
    darkorchid: "#9932cc",
    darkred: "#8b0000",
    darksalmon: "#e9967a",
    darkviolet: "#9400d3",
    fuchsia: "#ff00ff",
    gold: "#ffd700",
    green: "#008000",
    indigo: "#4b0082",
    lime: "#00ff00",
    magenta: "#ff00ff",
    maroon: "#800000",
    navy: "#000080",
    olive: "#808000",
    orange: "#ffa500",
    pink: "#ffc0cb",
    purple: "#800080",
    violet: "#800080",
    red: "#ff0000",
    silver: "#c0c0c0",
    white: "#ffffff",
    yellow: "#ffff00"

};

COLORS.list = function() {
    var result = [];
    for(var key in COLORS.names) {
        result.push(COLORS.names[key]);
    }
    return result;
};

function hexToRgb(hex) {
    hex = hex.slice(1, hex.length)
    var bigint = parseInt(hex, 16);
    var r = (bigint >> 16) & 255;
    var g = (bigint >> 8) & 255;
    var b = bigint & 255;

    return r + "," + g + "," + b;
}