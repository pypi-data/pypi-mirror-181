import pytest, os
from unittest.mock import call
from xxnlp.utils import set_directory
from freezegun import freeze_time
from xxnlp.project.twitter.models import Reminder
from xxnlp.project.twitter import bot, const


@pytest.mark.usefixtures("mock_mention_replies_to_another_tweet")
def test_creates_reminder_when_mention_is_a_reply_to_another_tweet(
    mock_alpha_vantage_get_intraday
):
    bot.reply_to_mentions()

    mock_alpha_vantage_get_intraday.assert_called_once_with("AMZN")
    assert Reminder.select().count() == 1
    assert Reminder.select().first().tweet_id == 2