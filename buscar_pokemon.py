import json

def formatar_pokemon(pokemon):
    evolutions = []
    abilities = []
    
    # Formatando evoluções
    evolucao_uniq = set()
    for evol in pokemon.get('evolutions', []):
        if evol['pokemon_id'] not in evolucao_uniq:
            evolucao_uniq.add(evol['pokemon_id'])
            evolutions.append(f"{evol['pokemon_name']} - {evol['pokemon_id']} - {evol['url']}")

    # Formatando habilidades
    for ability in pokemon.get('abilities', []):
        description = ability.get('description', 'Descrição não disponível')  # Verifica se 'description' existe
        abilities.append(f"{ability['name']} - {ability['url']} - {description}")
    
    # Formatando output final
    return {
        "Nome": pokemon.get("pokemon_name"),
        "URL": pokemon.get("evolutions")[0]["url"] if pokemon.get("evolutions") else None,
        "ID": pokemon.get("pokemon_id"),
        "Altura": pokemon.get("height").split("\xa0")[0],  # Remove qualquer espaço não quebrável
        "Peso": pokemon.get("weight").split("\xa0")[0],
        "Tipos": pokemon.get("types", []),
        "Habilidades": abilities,
        "Evoluções": evolutions
    }

def buscar_pokemon_por_id(pokedex_id, caminho_arquivo='pokemons.json'):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            pokemons = json.load(arquivo)

        for pokemon in pokemons:
            if pokemon.get('pokemon_id') == pokedex_id:
                resultado_formatado = formatar_pokemon(pokemon)
                return json.dumps(resultado_formatado, indent=4, ensure_ascii=False)

        return f"Pokémon com ID {pokedex_id} não encontrado."
    
    except FileNotFoundError:
        return f"Arquivo {caminho_arquivo} não encontrado."
    except json.JSONDecodeError:
        return "Erro ao ler o arquivo JSON. Verifique se o arquivo está formatado corretamente."

# Exemplo de uso
if __name__ == '__main__':
    pokedex_id = input("Digite o ID do Pokémon na Pokédex: ").zfill(4)
    print(buscar_pokemon_por_id(pokedex_id))
