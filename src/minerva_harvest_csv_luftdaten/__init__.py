# -*- coding: utf-8 -*-
from minerva_harvest_csv_luftdaten.parser_luftdaten import Parser
from minerva.harvest.plugin_api_trend import HarvestPluginTrend


class Plugin(HarvestPluginTrend):
    @staticmethod
    def create_parser(config):
        """Return parser instance."""
        return Parser(config)
