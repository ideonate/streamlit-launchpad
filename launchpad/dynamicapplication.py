import tornado.web


class DynamicApplication(tornado.web.Application):

    def remove_handlers(self, appname):

        remove_rules_index = -1

        for i, rule in enumerate(self.default_router.rules):
            print(rule)
            print(rule.matcher)

            if isinstance(rule.target, tornado.web.ReversibleRouter):
                print(rule.target.named_rules)
                if appname+ 'ws' in rule.target.named_rules or appname+ 'http' in rule.target.named_rules:
                    remove_rules_index = i

        if remove_rules_index >= 0:
            print("Remove rules {}".format(remove_rules_index))
            del self.default_router.rules[remove_rules_index]
