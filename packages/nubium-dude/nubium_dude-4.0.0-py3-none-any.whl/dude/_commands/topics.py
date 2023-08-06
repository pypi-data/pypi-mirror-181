import importlib
import json

import click

from . import dude_cli
from .cli_base import _init_kafka_toolbox, _pass_kafka_toolbox


def _get_cluster_for_topic(kafka_toolbox, topic):
    topics = kafka_toolbox.list_topics(by_topic=True)
    return topics[topic]


@dude_cli.group("topics")
@click.pass_context
def topics_group(ctx):
    ctx.obj = _init_kafka_toolbox(ctx)


@_pass_kafka_toolbox
def create_all_topics(kafka_toolbox, ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    kafka_toolbox.create_all_topics()
    ctx.exit()


@topics_group.command(name="create")
@_pass_kafka_toolbox
@click.option("--all", is_flag=True, expose_value=False, is_eager=True, callback=create_all_topics)
@click.option("--topics", type=str, required=True)
@click.option("--num-partitions", type=int, default=3)
@click.option("--replication-factor", type=int, default=3)
@click.option("--topic-config", type=dict, default={})
def create_topics(kafka_toolbox, topics, num_partitions, replication_factor, topic_config):
    cluster = next(iter(kafka_toolbox.admin_clients))
    kafka_toolbox.create_topics(
        {topic: cluster for topic in topics.split(",")},
        num_partitions=num_partitions,
        replication_factor=replication_factor,
        topic_config=topic_config,
    )


@topics_group.command(name="delete")
@_pass_kafka_toolbox
@click.option("--topics", type=str, required=True)
def delete_topics(kafka_toolbox, topics):
    for topic in topics.split(","):
        cluster = _get_cluster_for_topic(kafka_toolbox, topic)
        kafka_toolbox.delete_topics(
            {topic: cluster for topic in topics.split(",")},
        )


@topics_group.command(name="list")
@_pass_kafka_toolbox
@click.option("--by-topic", type=bool, default=False)
@click.option("--mirrors", type=bool, default=False)
def list_topics(kafka_toolbox, by_topic, mirrors):
    click.echo(
        json.dumps(
            kafka_toolbox.list_topics(
                by_topic=by_topic,
                mirrors=mirrors,
            ),
            indent=4,
        )
    )
