<script lang="ts">
    import { onMount } from "svelte";

    interface Game {
        id: number;
        title: string;
        description: string;
        publisher_name?: string;
        category_name?: string;
    }

    export let games: Game[] = [];
    let loading = true;
    let error: string | null = null;

    // Deterministic accent colours cycling per card
    const accents = [
        { border: "from-blue-500 to-cyan-400",   badge: "bg-blue-900/60 text-blue-300",   glow: "hover:shadow-blue-500/20"   },
        { border: "from-purple-500 to-pink-400",  badge: "bg-purple-900/60 text-purple-300", glow: "hover:shadow-purple-500/20" },
        { border: "from-emerald-500 to-teal-400", badge: "bg-emerald-900/60 text-emerald-300", glow: "hover:shadow-emerald-500/20" },
        { border: "from-orange-500 to-amber-400", badge: "bg-orange-900/60 text-orange-300", glow: "hover:shadow-orange-500/20" },
        { border: "from-rose-500 to-pink-400",    badge: "bg-rose-900/60 text-rose-300",   glow: "hover:shadow-rose-500/20"   },
        { border: "from-sky-500 to-indigo-400",   badge: "bg-sky-900/60 text-sky-300",     glow: "hover:shadow-sky-500/20"    },
    ];

    // Deterministic mock funding percentage (seeded on id).
    // Multiplier 37 and modulus 71 spread values across the 30–100 range
    // without clustering, giving visually varied but reproducible progress bars.
    function mockFunding(id: number): number {
        return Math.min(100, 30 + ((id * 37) % 71));
    }

    const fetchGames = async () => {
        loading = true;
        try {
            const response = await fetch('/api/games');
            if(response.ok) {
                games = await response.json();
            } else {
                error = `Failed to fetch data: ${response.status} ${response.statusText}`;
            }
        } catch (err) {
            error = `Error: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            loading = false;
        }
    };

    onMount(() => {
        fetchGames();
    });
</script>

<div>
    <div class="flex items-center gap-3 mb-8">
        <h2 class="text-2xl font-bold text-slate-100">Featured Games</h2>
        <span class="h-px flex-1 bg-gradient-to-r from-slate-700 to-transparent"></span>
    </div>
    
    {#if loading}
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each Array(6) as _, i}
                <div class="bg-slate-800/60 backdrop-blur-sm rounded-2xl overflow-hidden shadow-lg border border-slate-700/50">
                    <div class="h-1 bg-slate-700/60"></div>
                    <div class="p-6">
                        <div class="animate-pulse">
                            <div class="h-6 bg-slate-700 rounded-lg w-3/4 mb-3"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/2 mb-4"></div>
                            <div class="h-3 bg-slate-700 rounded w-full mb-2"></div>
                            <div class="h-3 bg-slate-700 rounded w-5/6 mb-4"></div>
                            <div class="h-1.5 bg-slate-700 rounded-full w-full mb-2"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/4 mt-4"></div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if error}
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700">
            <p class="text-red-400">{error}</p>
        </div>
    {:else if games.length === 0}
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700">
            <p class="text-slate-300">No games available at the moment.</p>
        </div>
    {:else}
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="games-grid">
            {#each games as game, i (game.id)}
                {@const accent = accents[i % accents.length]}
                {@const funding = mockFunding(game.id)}
                <a 
                    href={`/game/${game.id}`}
                    class="group relative flex flex-col bg-slate-800/70 backdrop-blur-sm rounded-2xl overflow-hidden shadow-lg border border-slate-700/40 hover:border-slate-600/60 hover:shadow-xl {accent.glow} transition-all duration-300 hover:-translate-y-1.5"
                    data-testid="game-card"
                    data-game-id={game.id}
                    data-game-title={game.title}
                >
                    <!-- Coloured gradient top bar -->
                    <div class="h-1 w-full bg-gradient-to-r {accent.border}"></div>

                    <div class="p-6 flex flex-col flex-1">
                        <!-- Faint gradient overlay on hover -->
                        <div class="absolute inset-0 bg-gradient-to-br from-white/[0.02] to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>

                        <!-- Title + badges -->
                        <div class="relative z-10 flex-1">
                            <h3 class="text-lg font-bold text-slate-100 mb-3 group-hover:text-white transition-colors leading-snug" data-testid="game-title">
                                {game.title}
                            </h3>

                            {#if game.category_name || game.publisher_name}
                                <div class="flex flex-wrap gap-2 mb-3">
                                    {#if game.category_name}
                                        <span class="text-xs font-medium px-2.5 py-0.5 rounded-full {accent.badge}" data-testid="game-category">
                                            {game.category_name}
                                        </span>
                                    {/if}
                                    {#if game.publisher_name}
                                        <span class="text-xs font-medium px-2.5 py-0.5 rounded-full bg-slate-700/60 text-slate-300" data-testid="game-publisher">
                                            {game.publisher_name}
                                        </span>
                                    {/if}
                                </div>
                            {/if}

                            <p class="text-slate-400 text-sm leading-relaxed line-clamp-2 mb-4" data-testid="game-description">
                                {game.description}
                            </p>
                        </div>

                        <!-- Funding progress -->
                        <div class="relative z-10 mb-4">
                            <div class="flex justify-between items-center mb-1.5">
                                <span class="text-xs text-slate-400 font-medium">Funding progress</span>
                                <span class="text-xs font-bold text-slate-200">{funding}%</span>
                            </div>
                            <div class="h-1.5 w-full bg-slate-700 rounded-full overflow-hidden">
                                <div class="h-full rounded-full bg-gradient-to-r {accent.border} transition-all duration-700" style="width: {funding}%"></div>
                            </div>
                        </div>

                        <!-- View details link -->
                        <div class="relative z-10 mt-auto pt-3 border-t border-slate-700/50 flex items-center justify-between">
                            <span class="text-sm font-semibold text-blue-400 group-hover:text-blue-300 flex items-center gap-1.5 transition-colors">
                                View details
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transform transition-transform duration-300 group-hover:translate-x-1.5" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                            </span>
                            <span class="text-xs text-slate-500 font-medium">Back this →</span>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
</div>