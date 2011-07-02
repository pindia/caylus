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
        $(this).append('<div class="span-3 worker last">&nbsp;</div>');
        //$(this).append('<div class="span-1 worker">&nbsp;</div>');
        //$(this).append('<div class="span-1 last">&nbsp;</div>');
        $(this).append('<div class="span-3 label last">&nbsp;</div>'); 
    });
    

    
    for(var i=0; i<TRACKS.length; i++){
        $('#favors').append('<tr id="t' + i + '"></tr>')
        $('#favors').children(':last').append('<td id="t'+i+'c-1">-</td>')
        for(var j=0; j<TRACKS[i].length; j++){
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
    /*turn_order = ''
    for(var i=0; i<DATA.players.length; i++){
        turn_order += DATA.players[i].name + '<br>';
    }
    $('#order').html(turn_order)*/
    
    // Update buildings
    
    for(var i=0; i<DATA.buildings.length; i++){
        update_building(i);
    }
    
    $('#b0 .worker').html('&nbsp;')
    for(var i=0; i<DATA.castle_order.length; i++){
        $('#b0 .worker').append(piece_image('worker', DATA.castle_order[i]))
    }
    
    $('#b5 .worker').html('&nbsp;')
    for(var i=0; i<DATA.stables_order.length; i++){
        $('#b5 .worker').append(piece_image('worker', DATA.stables_order[i]))
        
    }
    
    if(DATA.bailiff < 11)
        $('#b18 .bailiff').text('D')
    if(DATA.bailiff < 17)
        $('#b24 .bailiff').text('W')
    if(DATA.bailiff < 23)
        $('#b30 .bailiff').text('T')
    
    // Update player status markers
    
    for(var i=0; i<DATA.players.length; i++){
        update_player(i)
    }
    
    // Update bridge
    if(!DATA.pass_order){
        $('#bridge').text('No players have passed.')
    } else{
        $('#bridge').text('Passed: ' + DATA.pass_order)
    }
    
    // Update castle tracker
    $('#castle-tracker').text('')
    for(var i=0; i<DATA.players.length; i++){
        player = DATA.players[i]
        $('#castle-tracker').append(player.name + ': ' + player.section_batches[DATA.section])
    }
    
        
    // Create the red highlight
    
    $('*').removeClass('current')
    if(DATA.phase == 2)
        $('#b' + (DATA.step + 2)).addClass('current')
    if(DATA.phase == 3)
        $('#bridge').addClass('current')
    if(DATA.phase == 4){
        $('#b' + (DATA.step + 7)).addClass('current')
    }
    if(DATA.phase == 5 || DATA.phase == 6)
        $('#b0').addClass('current')
    
    if(DATA.current_decision && DATA.current_decision.player == PLAYER){
        show_decision()
    }
}

function player_initial(player){
    if(player == 'Black')
        return 'K'
    return player[0]
}

function static_piece_image(type, display){
    if(!display)
        return '&nbsp;'
    return '<img src="/static/img/pieces/' + type + '.png">';
}

function piece_image(type, player){
    if(!player)
        return '&nbsp;'
    return '<img src="/static/img/pieces/' + type + player_initial(player) + '.png">';
}

function update_building(i){
    building = DATA.buildings[i]
    if(i == 6)
        building.owner = DATA.inn_player
    element = $('#b' + i)
    element.removeClass('neutral wood stone residence prestige null fixed')
    element.addClass(building.type)
    element.find('.label').text(building.repr)
    element.find('.provost').html(static_piece_image('provost', DATA.provost == i-7))
    element.find('.bailiff').html(static_piece_image('bailiff', DATA.bailiff == i-7))
    element.find('.owner').html(piece_image('house',building.owner))
    element.find('.worker').html(piece_image('worker',building.worker))
}

function update_player(i){
    player = DATA.players[i]
    $('#p{0}n'.format(i)).text(player.name)
    $('#p{0}p'.format(i)).text(player.resources['points'] + 'P')
    $('#p{0}m'.format(i)).text('$' + player.resources['money'])
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
    
    // Royal favor board
    $('.rf' + i).remove()
    for(var j=0; j<player.favors.length; j++){
        k = player.favors[j]
        element = $('#t'+j+'c'+k)
        element.append(piece_image('worker', player.name))
        element.children().last().attr('width', 5).addClass('rf'+i)
    }
}

function show_decision(){
    DECISION = DATA.current_decision
    if(DATA.current_decision.cls == 'WorkerDecision'){
        show_worker_decision()
    } else if(DATA.current_decision.cls == 'ActionDecision' ||
              DATA.current_decision.cls == 'FavorDecision'){
        show_action_decision()
    } else if(DATA.current_decision.cls == 'FavorTrackDecision'){
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
    dialog = DIALOG
    DIALOG = null
    $.post('submit', {'id':GAME_ID, 'i':i}, function(data){
        dialog.dialog('close')
    });
}

function update_received(message){
    if(DIALOG){
        DIALOG.dialog('close')
        DIALOG = null
    }
    DATA = $.parseJSON(message)
    update_board()
    //show_decision()
}

function show_connect_dialog(){
    var dialog = $('<div></div>')
    dialog.append('Game ID:<input type="entry" id="game-id" value="0" size="2"> Player:<input type="entry" id="player" value="0" size="2">')
    dialog.append('<br>Create: <input type="checkbox" id="create">')
    dialog.append('<br><input type="button" value="Connect">');
    dialog.children('input[type="button"]').click(perform_connect)
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
    dialog = DIALOG
    DIALOG = null
    $.getJSON('connect', params, function(data) {
        dialog.dialog('close')
        DATA = data
        init_board()
        update_board()
        updater.update_received = update_received
        updater.poll();
    });
}



$(document).ready(function(){
    setTimeout(show_connect_dialog, 1000);
    $('.b').click(function(){
        if($(this).hasClass('available')){
            $('.b').removeClass('available')
            submit_decision($(this).attr('i'))
        }
    })
    //DECISION = ACTION_DECISION
    //show_action_decision()
});