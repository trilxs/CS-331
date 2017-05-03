/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
		edit by Xiaoyi Yang in 5-2-2017
		algorithm complete, adding comment

		explain here:
		at very first time I used state * succ to store child. But in that way I cant use for/while loop to get size value.
		So I change to List. In this way, I can store size value. using push to add and pop to remove.
 */
#include <iostream>
#include <assert.h>
#include "MinimaxPlayer.h"
#include <algorithm>  //lib for min()/max()
#include <list>		//lib for list
using namespace std;

using std::vector;
char current_symbol; //create a global symbol for current move player.

MinimaxPlayer::MinimaxPlayer(char symb) :
		Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}

void MinimaxPlayer::get_move(OthelloBoard* b, int& col, int& row) {
    // To be filled in by you
	//cout << " Hi" << endl;
	current_symbol = symbol;
	int best_move = 0;
	int best_val = -100;
	//int num = 0;
	//char symbol;
	//create node
	state New_node, result;
	New_node.b = new OthelloBoard(*b);
	list <MinimaxPlayer::state> children = Successor(New_node);

	while(!children.empty()) {
		state temp_node = children.front();
		int temp_val = Min_value(temp_node);
		if (temp_val > best_val) {
			best_val = temp_val;
			result = temp_node;
		}
		children.pop_front();
	}
	//now set the col and row to best move
	//cout << temp_succ[best_move].col << "  " << endl;
	//cout << temp_succ[best_move].row << "  " << endl;
	col = result.col;
	row = result.row;
	
}

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}

/* 
Plan:

Function: Minimax_decision(state) return action put in move_to(get_move)

Function: Max_value(state) return utility value complete

Function: Min_value(state) return utility value complete

Function: Successor(state) complete

Function: Utility(state) complete
*/

/*
std::list<state> MinimaxPlayer::Successor(state node)
{
return std::list<state>();
}
*/

//function should has ability to create all possible moves.
list<MinimaxPlayer::state> MinimaxPlayer::Successor(MinimaxPlayer::state node) {
	list <MinimaxPlayer::state> temp;
	int count = 0;
	for (int i = 0; i < node.b->get_num_cols(); i++) {
		for (int j = 0; j < node.b->get_num_rows(); j++) {
			if (node.b->is_legal_move(i, j, current_symbol)) {
				//create the new board.
				MinimaxPlayer::state New_node;
				New_node.b = new OthelloBoard(*node.b);
				New_node.b->play_move(i, j, current_symbol);
				New_node.col = i;
				New_node.row = j;
				New_node.value = 0;
				//New_node.depth = node.depth + 1;
				//put New_node into *succ, then make a new one.
				temp.push_back(New_node);
				//count++;

			}
		}
	}
	return temp; //return all legal move.
}


//This one should return the value, or calls it cost? score value in current board(or just a given board)
int MinimaxPlayer::Utility(state node) {
	int p1 = node.b->count_score(node.b->get_p1_symbol());
	int p2 = node.b->count_score(node.b->get_p2_symbol());
	//return the score "value"
	return p1 - p2;
}

int MinimaxPlayer::Max_value(state node){
	//char symbol;
	if (node.b->has_legal_moves_remaining(node.b->get_p1_symbol())&& node.b->has_legal_moves_remaining(node.b->get_p2_symbol())) {
		int Max_val = -999999; //initialize Max value to lowest
		int num = 0;  //initialize number of successor
		current_symbol = node.b->get_p1_symbol(); //concerned player1, our great mankind to be player1. XD
		//Why did I think node is a good idea?
		

		//create children nodes. for all legal moves.
		//MinimaxPlayer::state *temp_succ = new MinimaxPlayer::state[sizeSucc];
		list <MinimaxPlayer::state> children = Successor(node);

		while (!children.empty()) {
			//children[i].depth = depth + 1;
			state temp_node = children.front();
			int temp = Min_value(temp_node);
			Max_val=max(Max_val, temp);
			children.pop_front();

		}
		return Max_val;
	}
	else
		return Utility(node);


}

int MinimaxPlayer::Min_value(state node) {
	//copy code is stupid...
	if (node.b->has_legal_moves_remaining(node.b->get_p1_symbol())&& node.b->has_legal_moves_remaining(node.b->get_p2_symbol())) {
		int Min_val = 999999; //initialize Min value to highest
		current_symbol = node.b->get_p2_symbol(); //concerned player2, only for AI
										  //Why did I think node is a good idea?

											  //create children nodes. for all legal moves.
		//MinimaxPlayer::state *temp_succ = new MinimaxPlayer::state[sizeSucc];
		list <MinimaxPlayer::state> children = Successor(node);

		while (!children.empty()) {
			//children[i].depth = depth + 1;
			state temp_node = children.front();
			int temp = Max_value(temp_node);
			Min_val = min(temp, Min_val);
			children.pop_front();
		}
		return Min_val;
	}
	else
		return Utility(node);
}

