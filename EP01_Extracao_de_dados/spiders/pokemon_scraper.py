import scrapy

class PokemonScraper(scrapy.Spider):
    name = 'pokemon'
    allowed_domains = ["pokemondb.net"]
    start_urls = ["https://pokemondb.net/pokedex/all"]

    def parse(self, response):
        # Seleciona todos os Pokémon na tabela da página inicial
        pokemons = response.css('#pokedex > tbody > tr')
        
        for pokemon in pokemons:
            link = pokemon.css("td.cell-name > a::attr(href)").get()
            if link:
                yield response.follow(link, self.parse_pokemon)

    def parse_pokemon(self, response):
        # Extrai as informações básicas
        pokemon_name = response.css('#main > h1::text').get()
        pokemon_id = response.css('.vitals-table > tbody > tr:contains("National №") > td strong::text').get()
        height = response.css('.vitals-table > tbody > tr:contains("Height") > td::text').get()
        weight = response.css('.vitals-table > tbody > tr:contains("Weight") > td::text').get()
        types = response.css('.vitals-table > tbody > tr:contains("Type") > td a::text').getall()

        # Extrai informações sobre evoluções
        evolutions = []
        evolution_section = response.css('div.infocard-list-evo a.ent-name')
        for evo in evolution_section:
            evo_link = evo.css('::attr(href)').get()
            evo_id = evo_link.split('/')[-1]
            evolutions.append({
                'pokemon_id': evo_id,
                'pokemon_name': evo.css('::text').get(),
                'url': response.urljoin(evo_link),
            })


        # Extrai habilidades e suas descrições
        abilities = []
        ability_rows = response.css('.vitals-table > tbody > tr:contains("Abilities") td a')
        for ability in ability_rows:
            ability_url = ability.css('::attr(href)').get()
            ability_name = ability.css('::text').get()
            ability_description = ability.css('::attr(title)').get()  # Extrai a descrição da habilidade (através do atributo title)

            abilities.append({
                'name': ability_name,
                'url': response.urljoin(ability_url),
                'description': ability_description  # Adiciona a descrição extraída
            })

        # Junta os dados
        yield {
            'pokemon_name': pokemon_name,
            'pokemon_id': pokemon_id.strip() if pokemon_id else None,
            'height': height.strip() if height else None,
            'weight': weight.strip() if weight else None,
            'types': types,
            'evolutions': list({e['url']: e for e in evolutions}.values()),  # Remove duplicatas de evoluções
            'abilities': abilities,
        }
