DATA = {"buildings": [{"owner": null, "worker": null, "class": "CastleBuilding", "repr": "Castle", "name": "Castle"}, {"owner": null, "worker": 'Blue', "class": "GateBuilding", "repr": "Gate", "name": "Gate"}, {"owner": 'Red', "worker": null, "class": "Building", "repr": "3", "name": "Trading Post"}, {"owner": null, "worker": null, "class": "GuildBuilding", "repr": "Prov", "name": "Merchant's Guild"}, {"owner": null, "worker": null, "class": "Building", "repr": "1C->RF", "name": "Joust Field"}, {"owner": null, "worker": null, "class": "StablesBuilding", "repr": "Stables", "name": "Stables"}, {"owner": null, "worker": null, "class": "InnBuilding", "repr": "Inn", "name": "Inn"}, {"owner": null, "worker": null, "class": "MarketBuilding", "repr": "R->4", "name": "Market"}, {"owner": null, "worker": null, "class": "Building", "repr": "S", "name": "Quarry"}, {"owner": null, "worker": null, "class": "CarpenterBuilding", "repr": "Carpenter", "name": "Carpenter"}, {"owner": null, "worker": null, "class": "Building", "repr": "W", "name": "Sawmill"}, {"owner": null, "worker": null, "class": "Building", "repr": "F/W", "name": "Forest"}, {"owner": null, "worker": null, "class": "Building", "repr": "F/C", "name": "Farm"}, {"owner": null, "worker": null, "class": "PeddlerBuilding", "repr": "2->R", "name": "Peddler"}, {"owner": null, "worker": null, "class": "CarpenterBuilding", "repr": "Carpenter", "name": "Carpenter"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "Building", "repr": "G", "name": "Gold Mine"}], "players": [{"name": "Blue", "favors": [-1, -1, -1, -1], "workers": 6, "section_batches": [0, 0, 0], "passed": false, "resources": {"stone": 0, "gold": 0, "food": 2, "money": 5, "cloth": 0, "wood": 1, "points": 0}}], "stables_order": [], "section": 0, "provost": 5, "bailiff": 5, "turn": 0, "step": 0, "pass_order": [], "phase": 0, "castle_order": []}
RESOURCES = ['food','wood','stone','cloth','gold']
TRACKS = [["P", "PP", "PPP", "PPPP", "PPPPP"], ["3", "4", "5", "6", "7"], ["F", "W/S", "C", "RR->R", "G"], ["-", "Carp", "Mason", "Lawyer", "Arch"]]
PLAYERS = ['Blue', 'Red', 'Green', 'Orange', 'Black']
GAME_ID = null
PLAYER_ID = null
DIALOG = null

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
        $(this).append('<div class="span-1 bailiff">&nbsp;</div>');
        $(this).append('<div class="span-1 provost">&nbsp;</div>');
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
    
    for(var i=0; i<DATA.buildings.length; i++){
        update_building(i);
    }
    for(var i=0; i<DATA.players.length; i++){
        update_player(i)
    }
    
    if(DATA.current_decision && DATA.current_decision.player == PLAYER){
        show_decision()
    }
}

function update_building(i){
    building = DATA.buildings[i]
    element = $('#b' + i)
    element.children('.label').text(building.repr)
    element.children('.provost').html(DATA.provost == i-7 ? 'O' : '&nbsp;')
    element.children('.bailiff').html(DATA.bailiff == i-7 ? 'B' : '&nbsp;')
    element.children('.owner').html(building.owner ? building.owner[0] : '&nbsp;')
    element.children('.worker').html(building.worker ? building.worker[0] : '&nbsp;')
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

function show_decision(){
    DECISION = DATA.current_decision
    if(DATA.current_decision.class == 'WorkerDecision'){
        show_worker_decision()
    } else if(DATA.current_decision.class == 'ActionDecision' ||
              DATA.current_decision.class == 'FavorDecision'){
        show_action_decision()
    } else if(DATA.current_decision.class == 'FavorTrackDecision'){
        show_favor_track_decision()
    }
}


function show_action_decision(){
    var dialog = $('<div></div>').hide()
    for(var i=0; i<DECISION.actions.length; i++){
        dialog.append('<input type="button" i="'+i+'"value="'+DECISION.actions[i].repr+'">')
        dialog.children().last().click(button_clicked)
    }
    dialog.dialog({title:'Select Action', closeOnEscape:false});
    dialog.closest('.ui-dialog').find('.ui-dialog-titlebar-close').hide();
    DIALOG = dialog

}

function show_worker_decision(){
    var dialog = $('<div></div>').hide()
    dialog.append('Click a building or <input type="button" i="0" value="Pass">')
    dialog.children().last().click(function(){
        $('.b').removeClass('available')
        submit_decision($(this).attr('i'))
    });
    console.log(DECISION.buildings)
    for(var i=0; i<DECISION.buildings.length; i++){
        building = DECISION.buildings[i]
        if(building != null){
            $('#b' + building.i).addClass('available')
            $('#b' + building.i).attr('i', i)
        }
    }
    dialog.dialog({title:'Worker Placement', closeOnEscape:false, minHeight:50});
    dialog.closest('.ui-dialog').find('.ui-dialog-titlebar-close').hide();
    DIALOG = dialog
}

function show_favor_track_decision(){
    var dialog = $('<div></div>').hide()
    for(var i=0; i<DECISION.tracks.length; i++){
        dialog.append('<input type="button" i="'+i+'"value="'+DECISION.tracks[i]+'">')
        dialog.children().last().click(button_clicked)
    }
    dialog.dialog({title:'Royal Favor', closeOnEscape:false});
    dialog.closest('.ui-dialog').find('.ui-dialog-titlebar-close').hide();
    DIALOG = dialog

}

function button_clicked(){
    submit_decision( $(this).attr('i') )
}

function submit_decision(i){
    $('.ui-dialog-content').text('Submitting... ' + i)
    $.post('submit', {'id':GAME_ID, 'i':i}, function(data){
        DIALOG.dialog('close')
        DIALOG = null
    });
}

function update_received(message){
    if(!DIALOG){
        DATA = $.parseJSON(message.data)
        update_board()
    } else {
        console.log('Warning: Ignoring update')
    }
    //show_decision()
}

function show_connect_dialog(){
    var dialog = $('<div></div>').hide()
    dialog.append('Game ID:<input type="entry" id="game-id" value="0" size="2"> Player:<input type="entry" id="player" value="0" size="2">')
    dialog.append('<br>Create: <input type="checkbox" id="create">')
    dialog.append('<br><input type="button" value="Connect"');
    dialog.children().last().click(perform_connect)
    dialog.dialog({title:'Connect to Server', closeOnEscape:false});
    dialog.closest('.ui-dialog').find('.ui-dialog-titlebar-close').hide();
    DIALOG = dialog    
}

function perform_connect(){
    PLAYER_ID = $('#create').is(':checked') ? 0 : parseInt($('#player').val());
    PLAYER = PLAYERS[PLAYER_ID]
    GAME_ID = $('#game-id').attr('value')
    params = {'id':$('#game-id').attr('value'),
              'player':$('#player').attr('value'),
              'create':($('#create').is(':checked') ? '1' : '0')}
    $('.ui-dialog-content').text('Connecting... ' )
    $.getJSON('connect', params, function(data) {
        DIALOG.dialog('close')
        DATA = data
        init_board()
        update_board()
        channel = new goog.appengine.Channel(DATA.players[PLAYER_ID].channel);
        socket = channel.open();
        socket.onmessage = update_received;
    });
}



$(document).ready(function(){
    show_connect_dialog();
    $('.b').click(function(){
        if($(this).hasClass('available')){
            $('.b').removeClass('available')
            submit_decision($(this).attr('i'))
        }
    })
    //DECISION = ACTION_DECISION
    //show_action_decision()
});