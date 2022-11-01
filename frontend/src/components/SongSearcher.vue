<template>

    <div>

        <h1> Buscador de canciones</h1>
        <!-- Create a simple searcher -->
        <div class="field has-addons">
            <div class="control">
                <input class="input" type="text" placeholder="Nombre de la canción / Artista" v-model="search">
            </div>
            <div class="control">
                <button class="button is-primary" @click="searchSongs">Buscar</button>
            </div>
            <p v-if="this.message.length > 0">Mensaje: {{ this.message }}</p>
        </div>

        <!-- Create a table to show the results -->
        <div v-if="this.songs.length > 0">
            <table class="table is-fullwidth">
                <thead>
                    <tr>
                        <th>Título</th>
                        <th>Artista</th>
                        <th>Imagen</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="song in this.songs" :key="song.id">
                        <td>{{ song.titulo }}</td>
                        <td>{{ song.artista }}</td>
                        <td><img :src="song.imagen"></td>
                        <td><button class="button is-primary" @click="addToQueue(song.id)"> Añadir a cola</button></td>
                        <!-- <td>
                        <button class="button is-primary" @click="addSongToPlaylist(song.id)">Añadir a playlist</button>
                    </td> -->
                    </tr>
                </tbody>
            </table>
        </div>
    </div>


</template>

<script>

export default {
    data() {
        return {
            search: '',
            songs: [],
            message: ''
        }
    },

    methods: {
        async searchSongs() {

            try {
                let response = await fetch('http://localhost:8000/search?query=' + this.search, {
                    headers: {
                        'access-token': localStorage.getItem('access-token')
                    },
                    method: 'POST'
                });
                let data = await response.json();
                this.songs = data.songs;
                console.log(this.songs);
            }

            catch (error) {
                console.log(error);
            }
        },

        async addToQueue(songId) {
            try {
                let response = await fetch('http://localhost:8000/add-song-to-queue/' + songId, {
                    headers: {
                        'access-token': localStorage.getItem('access-token')
                    },
                    method: 'POST'
                })

                let data = await response.json();
                console.log(data);
                this.message = data.message;


            } catch (e) {
                console.log(e);
            }

        }
    }
}

</script>

<style>

</style>