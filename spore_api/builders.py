import re
from typing import Any, Dict, List

from spore_api.constants import BASE_URL

from .utils import datatime_from_string
from .abc import ABCBuilder
from .enums import AssetType, AssetSubtype
from .models import (
    Achievement,
    Achievements,
    AssetComments,
    Assets,
    Buddies,
    Buddy,
    Comments,
    FullAsset,
    Sporecast,
    Sporecasts,
    Stats,
    Creature,
    Asset,
    SporecastAssets,
    Comment,
    User
)


class StatsBuilder(ABCBuilder):
    """
    Build stats
    http://www.spore.com/rest/stats
    """
    def build(self, raw_data: str) -> Stats:
        data: Dict[str, str] = self._decoder(raw_data)["stats"]

        return Stats(
            total_uploads=int(data["totalUploads"]),
            day_uploads=int(data["dayUploads"]),
            total_users=int(data["totalUsers"]),
            day_users=int(data["dayUsers"])
        )


class CreatureBuilder(ABCBuilder):
    """
    [Pages]

    Creature stats:
    http://www.spore.com/rest/creature/<CreatureAssetId>
    """
    def build(self, raw_data: str) -> Creature:
        data: Dict[str, str] = self._decoder(raw_data)["creature"]

        return Creature(
            cost=int(data["cost"]),
            health=float(data["health"]),
            height=float(data["height"]),
            meanness=float(data["meanness"]),
            cuteness=float(data["cuteness"]),
            sense=float(data["sense"]),
            bonecount=float(data["bonecount"]),
            footcount=float(data["footcount"]),
            graspercount=float(data["graspercount"]),
            basegear=float(data["basegear"]),
            carnivore=float(data["carnivore"]),
            herbivore=float(data["herbivore"]),
            glide=float(data["glide"]),
            sprint=float(data["sprint"]),
            stealth=float(data["stealth"]),
            bite=float(data["bite"]),
            charge=float(data["charge"]),
            strike=float(data["strike"]),
            spit=float(data["spit"]),
            sing=float(data["sing"]),
            dance=float(data["dance"]),
            gesture=float(data["gesture"]),
            posture=float(data["posture"]),
        )


class UserBuilder(ABCBuilder):
    """
    [Pages]

    Profile Info:
    http://www.spore.com/rest/user/<Username>
    """
    def build(self, raw_data: str) -> User:
        data: Dict[str, str] = self._decoder(raw_data)["user"]

        return User(
            id=int(data["id"]),
            image_url=data["image"],
            tagline=data["tagline"],
            create_at=datatime_from_string(data["creation"])
        )


class AssetsBuilder(ABCBuilder):
    """
    [Pages]

    Assets for user:
    http://www.spore.com/rest/assets/user/<Username>/<StartIndex>/<Length>

    Special Searches:
    http://www.spore.com/rest/assets/search/<ViewType>/<StartIndex>/<Length>
    """
    def build(self, raw_data: str) -> Assets:
        data: Dict[str, Any] = self._decoder(raw_data)["assets"]
        raw_assets: List[Dict[str, str]] = data["asset"]

        return Assets(
            assets=[
                Asset(
                    id=int(raw_asser["id"]),
                    name=raw_asser["name"],
                    thumbnail_url=raw_asser["thumb"],
                    image_url=raw_asser["image_url"],
                    author_name=raw_asser["author"],
                    create_at=datatime_from_string(raw_asser["created"]),
                    rating=float(raw_asser["rating"]),
                    type=AssetType(raw_asser["type"]),
                    subtype=AssetSubtype(raw_asser["subtype"]),
                    parent_id=int(raw_asser["parent"]),
                    description=raw_asser["description"],
                    tags=(
                        None
                        if raw_asser["tags"] == "NULL" else
                        raw_asser["tags"].split(", ")
                    ),
                )
                for raw_asser in raw_assets
            ]
        )


class SporecastsBuilder(ABCBuilder):
    """
    [Pages]

    Sporecasts for user:
    http://www.spore.com/rest/sporecasts/<Username>
    """

    def build(self, raw_data: str) -> Sporecasts:
        data: Dict[str, Any] = self._decoder(raw_data)["sporecasts"]
        raw_sporecast: List[Dict[str, str]] = data["sporecast"]

        return Sporecasts(
            sporecasts=[
                Sporecast(
                    id=int(raw_sporecast["id"]),
                    title=raw_sporecast["title"],
                    subtitle=raw_sporecast["subtitle"],
                    author_name=raw_sporecast["author"],
                    update_at=datatime_from_string(raw_sporecast["updated"]),
                    rating=float(raw_sporecast["rating"]),
                    subscription_count=int(raw_sporecast["subscriptioncount"]),
                    tags=re.sub(r"\W", " ", raw_sporecast["tags"]).split(),
                    assets_count=int(raw_sporecast["count"])
                )
                for raw_sporecast in raw_sporecast
            ]
        )


class SporecastAssetsBuilder(ABCBuilder):
    """
    [Pages]

    Assets for sporecast:
    http://www.spore.com/rest/assets/sporecast/<Sporecast Id>/<StartIndex>/<Length>
    """
    def build(self, raw_data: str) -> SporecastAssets:
        data: Dict[str, Any] = self._decoder(raw_data)["assets"]
        raw_assets: List[Dict[str, str]] = data["asset"]

        return SporecastAssets(
            name=data["name"],
            assets=[
                Asset(
                    id=int(raw_asser["id"]),
                    name=raw_asser["name"],
                    thumbnail_url=raw_asser["thumb"],
                    image_url=raw_asser["image_url"],
                    author_name=raw_asser["author"],
                    create_at=datatime_from_string(raw_asser["created"]),
                    rating=float(data["rating"]),
                    type=AssetType(data["type"]),
                    subtype=AssetSubtype(data["subtype"]),
                    parent_id=int(data["parent"]),
                    description=data["description"],
                    tags=(
                        None
                        if data["tags"] == "NULL" else
                        data["tags"].split(",")
                    )
                )
                for raw_asser in raw_assets
            ]
        )


class AchievementsBuilder(ABCBuilder):
    """
    [Pages]

    Achievements for user:
    http://www.spore.com/rest/assets/achievements/<Username>/<StartIndex>/<Length>
    """
    def build(self, raw_data: str) -> Achievements:
        data: Dict[str, Any] = self._decoder(raw_data)["achievements"]
        raw_achievements: List[Dict[str, str]] = data["achievement"]

        return Achievements(
            achievements=[
                Achievement(
                    guid=raw_achievement["guid"],
                    image_url=f"{BASE_URL}/static/war/images/achievements/{raw_achievement['guild']}.png",
                    date=datatime_from_string(raw_achievement["date"])
                )
                for raw_achievement in raw_achievements
            ]
        )


class FullAssetBuilder(ABCBuilder):
    """
    [Pages]

    Info about an asset:
    http://www.spore.com/rest/asset/<AssetId>
    """
    def build(self, raw_data: str) -> FullAsset:
        data: Dict[str, Any] = self._decoder(raw_data)["achievements"]
        raw_comments: List[Dict[str, str]] = data["comments"]

        return FullAsset(
            id=int(data["id"]),
            name=data["name"],
            thumbnail_url=data["thumb"],
            image_url=data["image_url"],
            author_name=data["author"],
            create_at=datatime_from_string(data["created"]),
            rating=float(data["rating"]),
            type=AssetType(data["type"]),
            subtype=AssetSubtype(data["subtype"]),
            parent_id=int(data["parent"]),
            description=data["description"],
            tags=(
                None
                if data["tags"] == "NULL" else
                data["tags"].split(",")
            ),
            author_id=data["authorid"],
            comments=Comments(
                comments=[
                    Comment(
                        message=raw_comment["message"],
                        sender_name=raw_comment["sender"]
                    )
                    for raw_comment in raw_comments
                ]
            )
        )


class AssetCommentsBuilder(ABCBuilder):
    """
    [Pages]

    Comments for an asset:
    http://www.spore.com/rest/comments/<AssetId>/<StartIndex>/<Length>
    """
    def build(self, raw_data: str) -> AssetComments:
        data: Dict[str, Any] = self._decoder(raw_data)["comments"]
        raw_comments: List[Dict[str, str]] = data["comments"]

        return AssetComments(
            name=data["name"],
            comments=[
                Comment(
                    message=raw_comment["message"],
                    sender_name=raw_comment["sender"]
                )
                for raw_comment in raw_comments
            ]
        )


class BuddiesBuilder(ABCBuilder):
    """
    [Pages]

    Buddies for user:
    http://www.spore.com/rest/users/buddies/<Username>/<StartIndex>/<Length>

    Who has added a user as a buddy:
    http://www.spore.com/rest/users/subscribers/<Username>/<StartIndex>/<Length>
    """
    def build(self, raw_data: str) -> Buddies:
        data: Dict[str, Any] = self._decoder(raw_data)["users"]
        raw_buddy: List[Dict[str, str]] = data["buddy"]

        return Buddies(
            buddies=[
                Buddy(
                    name=raw_buddy["name"],
                    id=int(raw_buddy["id"])
                )
                for raw_buddy in raw_buddy
            ]
        )
