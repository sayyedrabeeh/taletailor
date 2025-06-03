from watchgod import run_process, DefaultWatcher
import os


# Custom watcher to include .html, .css, .js, .py
class TemplateWatcher(DefaultWatcher):
    def should_watch_file(self, entry):
        return entry.name.endswith(('.py', '.html', '.css', '.js'))


def run():
    from run_daphne import main
    main()


if __name__ == "__main__":
     run_process(os.getcwd(), run, watcher_cls=TemplateWatcher)
