import yaml

def options_parser():
  with open('mkdocs.yml', 'r') as stream:
    mkdocs_yaml = yaml.safe_load(stream)
  
  plugins = mkdocs_yaml['plugins']
  for plugin in plugins:
    if type(plugin) == dict:
      return plugin['with-pdf']

if __name__ == "__main__":
  print(options_parser())