from bughouse.ratings import rate_teams, rate_players, provisional_modifier

def test_rate_single_game(factories, models, elo_settings):
    game = factories.GameFactory()
    r1, r2 = rate_teams(game)
    assert r1.rating == 1008 
    assert r2.rating == 992


def test_rate_multiple_games(factories, models):
    team_a = factories.TeamFactory()
    team_b = factories.TeamFactory()
    r1 = rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    r2 = rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    
    assert team_a.latest_rating == 1020
    assert team_b.latest_rating == 980

def test_provisional_limit(factories, models):
    team_a = factories.TeamFactory()
    team_b = factories.TeamFactory()
   
    assert provisional_modifier(team_a) == 4
    
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
   
    assert provisional_modifier(team_a) == 4
    
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
   
    assert team_a.total_games == 11
    assert provisional_modifier(team_a) == 1
    assert team_a.latest_rating == 1120 
    assert team_b.latest_rating == 880


def test_individual_ratings(factories, models):
    game = factories.GameFactory()
    
    if game.losing_color == game.BLACK:    
        wtw, wtb, ltw, ltb = rate_players(game)
    
        assert wtw.player.latest_rating == 1012
        assert wtb.player.latest_rating == 1008 
        assert ltw.player.latest_rating == 992 
        assert ltb.player.latest_rating == 988 
    
    else:
        wtw, wtb, ltw, ltb = rate_players(game)
    
        assert wtw.player.latest_rating == 1008 
        assert wtb.player.latest_rating == 1012 
        assert ltw.player.latest_rating == 988
        assert ltb.player.latest_rating == 992 
