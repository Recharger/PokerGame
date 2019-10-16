from django.shortcuts import render, get_object_or_404
import json

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .utils import Player, Game


#    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
#    def register(self, request):
#        return self.create(request)


class GameViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    games = []

    def list(self, request):
        result = json.dumps({index:game.name() for index, game in enumerate(self.games)})
        return Response(result)

    def create(self, request):
        new_game = Game()
        self.games.append(new_game)
        return Response(self.games.index(new_game))

    def retrieve(self, request, pk=None):
        if pk > 0 and pk < len(self.games):
            game = self.games[pk]
            if len(game.get_winners()) > 0:
                for player in game.get_players():
                    if player.is_me(request.user):
                        if player in game.get_winners():
                            combination = game.check_hand(player)
                            return Response(json.dumps({"message": f"You win with {combination[0].name}, {combination[1]}"}), status=status.HTTP_200_OK)
                        else:
                            return Response(json.dumps({"message": "You lose"}), status=status.HTTP_200_OK)
            else:
                return Response(json.dumps({"message": "Game not played yet"}), status=status.HTTP_200_OK)

        else:
            return Response(json.dumps({"message": "No game with this pk"}), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if pk > 0  and pk < len(self.games):
            player = Player(request.user)
            try:
                games[pk].add_player(player)
                return Response('ok', status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(json.dumps({"message": "No game with this pk"}), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if pk > 0  and pk < len(self.games):
            del self.games[pk]
            return Response(json.dumps({"message": "Game deleted"}), status=status.HTTP_200_OK)
