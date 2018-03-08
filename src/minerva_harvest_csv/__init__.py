# -*- coding: utf-8 -*-
from minerva_harvest_csv.parser_aireas import Parser
import minerva_harvest_csv.abstractparser as abstractparser
from minerva.harvest.plugin_api_trend import HarvestPluginTrend


class Plugin(HarvestPluginTrend):
    @staticmethod
    def create_parser(config):
        """Return parser instance."""
        return Parser(config)
