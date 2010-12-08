DATA = {"buildings": [{"owner": null, "worker": null, "class": "CastleBuilding", "repr": "Castle", "name": "Castle"}, {"owner": null, "worker": 'Blue', "class": "GateBuilding", "repr": "Gate", "name": "Gate"}, {"owner": 'Red', "worker": null, "class": "Building", "repr": "3", "name": "Trading Post"}, {"owner": null, "worker": null, "class": "GuildBuilding", "repr": "Prov", "name": "Merchant's Guild"}, {"owner": null, "worker": null, "class": "Building", "repr": "1C->RF", "name": "Joust Field"}, {"owner": null, "worker": null, "class": "StablesBuilding", "repr": "Stables", "name": "Stables"}, {"owner": null, "worker": null, "class": "InnBuilding", "repr": "Inn", "name": "Inn"}, {"owner": null, "worker": null, "class": "MarketBuilding", "repr": "R->4", "name": "Market"}, {"owner": null, "worker": null, "class": "Building", "repr": "S", "name": "Quarry"}, {"owner": null, "worker": null, "class": "CarpenterBuilding", "repr": "Carpenter", "name": "Carpenter"}, {"owner": null, "worker": null, "class": "Building", "repr": "W", "name": "Sawmill"}, {"owner": null, "worker": null, "class": "Building", "repr": "F/W", "name": "Forest"}, {"owner": null, "worker": null, "class": "Building", "repr": "F/C", "name": "Farm"}, {"owner": null, "worker": null, "class": "PeddlerBuilding", "repr": "2->R", "name": "Peddler"}, {"owner": null, "worker": null, "class": "CarpenterBuilding", "repr": "Carpenter", "name": "Carpenter"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "Building", "repr": "G", "name": "Gold Mine"}], "players": [{"name": "Blue", "favors": [-1, -1, -1, -1], "workers": 6, "section_batches": [0, 0, 0], "passed": false, "resources": {"stone": 0, "gold": 0, "food": 2, "money": 5, "cloth": 0, "wood": 1, "points": 0}}], "stables_order": [], "section": 0, "provost": 5, "bailiff": 5, "turn": 0, "step": 0, "pass_order": [], "phase": 0, "castle_order": []}
ACTION_DECISION = {"player": "Blue", "class": "ActionDecision", "actions": [{"class": "NullAction", "repr": "(None)"}, {"class": "BribeProvostAction", "repr": "3->P-3"}, {"class": "BribeProvostAction", "repr": "2->P-2"}, {"class": "BribeProvostAction", "repr": "1->P-1"}, {"class": "BribeProvostAction", "repr": "1->P+1"}, {"class": "BribeProvostAction", "repr": "2->P+2"}, {"class": "BribeProvostAction", "repr": "3->P+3"}]}
RESOURCES = ['food','wood','stone','cloth','gold']
TRACKS = [["P", "PP", "PPP", "PPPP", "PPPPP"], ["3", "4", "5", "6", "7"], ["F", "W/S", "C", "RR->R", "G"], ["-", "Carp", "Mason", "Lawyer", "Arch"]]

String.prototype.format = function() {
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{'+i+'\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};


function init_board(){
    $('.b').each(function(i){
        $(this).text('')
        $(this).append('<div class="span-1">&nbsp;</div>');
        $(this).append('<div class="span-1">&nbsp;</div>');
        $(this).append('<div class="span-1 owner last">&nbsp;</div>');
        $(this).append('<div class="span-1">&nbsp;</div>');
        $(this).append('<div class="span-1 worker">&nbsp;</div>');
        $(this).append('<div class="span-1 last">&nbsp;</div>');
        $(this).append('<div class="span-3 label last">&nbsp;</div>'); 
    });
    
    for(var i=0; i<TRACKS.length; i++){
        $('#favors').append('<tr id="t' + i + '"></tr>')
        $('#favors').children(':last').append('<td id="t'+i+'c-1">-</td>')
        for(var j=0; j<TRACKS.length; j++){
            $('#favors').children(':last').append('<td id="t'+i+'c'+j+'">'+TRACKS[i][j]+'</td>')
        }
    }
    
    for(var i=0; i<DATA.players.length; i++){
        $('#players').append('<tr id="p{0}">'.format(i))
        $('#players').children(':last').append('<td id="p{0}n">-</td>'.format(i))
        $('#players').children(':last').append('<td id="p{0}p">-</td>'.format(i))
        $('#players').children(':last').append('<td id="p{0}m">-</td>'.format(i))
        $('#players').children(':last').append('<td id="p{0}r">-</td>'.format(i))
    }
}

function update_board(){
    turn_order = ''
    for(var i=0; i<DATA.players.length; i++){
        turn_order += DATA.players[i].name + '<br>';
    }
    $('#order').html(turn_order)
}

function update_building(i){
    building = DATA.buildings[i]
    element = $('#b' + i)
    element.children('.label').text(building.repr)
    element.children('.owner').text(building.owner ? building.owner[0] : '')
    element.children('.worker').text(building.worker ? building.worker[0] : '')
}

function update_player(i){
    player = DATA.players[i]
    $('#p{0}n'.format(i)).text(player.name)
    $('#p{0}p'.format(i)).text(player.resources['points'])
    $('#p{0}m'.format(i)).text(player.resources['money'])
    resources = ' '
    for(var j in RESOURCES){
        resource = RESOURCES[j]
        if(player.resources[resource] > 0)
        {
            for(var k=0; k<player.resources[resource]; k++){
                resources += resource[0].toUpperCase()
            }
            resources += ' '
        }
    }
    $('#p{0}r'.format(i)).text(resources)
}

function show_action_decision(){
    var dialog = $('<div></div>').hide()
    for(var i=0; i<DECISION.actions.length; i++){
        dialog.append('<input type="button" value="'+DECISION.actions[i].repr+'">')
    }
    dialog.dialog({title:'Select Action', closeOnEscape:false});
    dialog.closest('.ui-dialog').find('.ui-dialog-titlebar-close').hide();

}

function show_worker_decision(){
    var dialog = $('<div></div>').hide()
    dialog.append('Click a building or <input type="button" value="Pass">')
    dialog.dialog({title:'Worker Placement', closeOnEscape:false, minHeight:50});
    dialog.closest('.ui-dialog').find('.ui-dialog-titlebar-close').hide();    
}


$(document).ready(function(){
    init_board();
    update_board();
    for(var i=0; i<DATA.buildings.length; i++){
        update_building(i);
    }
    for(var i=0; i<DATA.players.length; i++){
        update_player(i)
    }
    DECISION = ACTION_DECISION
    show_worker_decision()
});