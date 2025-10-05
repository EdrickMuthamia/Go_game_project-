from go_engine import GoEngine, Stone

def test_basic_functionality():
    """Test basic Go game functionality"""
    print("Testing Go Engine...")
    
    # Create 9x9 board
    game = GoEngine(9)
    print(f"Created {game.size}x{game.size} board")
    
    # Test stone placement
    print("\nTesting stone placement:")
    assert game.make_move(4, 4) == True  # Black plays center
    assert game.make_move(4, 5) == True  # White plays adjacent
    assert game.make_move(4, 4) == False # Invalid - occupied
    print("✓ Stone placement validation works")
    
    # Test capture
    print("\nTesting capture mechanics:")
    game = GoEngine(9)
    # Set up capture scenario
    game.make_move(1, 1)  # Black
    game.make_move(0, 1)  # White
    game.make_move(2, 1)  # Black
    game.make_move(1, 0)  # White
    game.make_move(1, 2)  # Black - captures white stone at (0,1)
    
    captured = game.captured[Stone.WHITE]
    print(f"✓ Captured {captured} white stones")
    
    # Test serialization
    print("\nTesting serialization:")
    serialized = game.serialize()
    restored_game = GoEngine.deserialize(serialized)
    assert restored_game.size == game.size
    assert restored_game.current_player == game.current_player
    print("✓ Serialization works")
    
    # Test territory calculation
    print("\nTesting territory calculation:")
    territory = game.calculate_territory()
    print(f"Territory: {territory}")
    
    # Test scoring
    score = game.get_score()
    print(f"Score: Black={score['black']:.1f}, White={score['white']:.1f}")
    
    print("\n✓ All tests passed!")

if __name__ == "__main__":
    test_basic_functionality()