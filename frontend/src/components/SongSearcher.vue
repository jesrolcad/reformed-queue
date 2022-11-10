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

import { useToast } from "vue-toastification";

export default {
    data() {
        return {
            search: '',
            songs: []
        }
    },

    methods: {

        // Función para mostrar notificaciones. Recibe mensaje a enviar (message) y tipo de notificación (type), que toma valores "info" o "error"
        showNotification(message, type) {

            const toast = useToast();
            const options = {
                    position: "bottom-right", timeout: 3000, closeOnClick: true, pauseOnFocusLoss: true, pauseOnHover: true,
                    draggable: true, draggablePercent: 0.6, showCloseButtonOnHover: true, hideProgressBar: true, closeButton: "button",
                    icon: true, rtl: false
                }

            if (type == 'info') {
                toast.info(message, options);
            }

            else {
                toast.error(message, options);
            }

        },

        async searchSongs() {

            try {
                let response = await fetch('http://localhost:8000/search?query=' + this.search, {
                    headers: {
                        'access-token': localStorage.getItem('access-token')
                    },
                    method: 'POST'
                });
                let status_code = response.status;
                let data = await response.json();

                if (status_code == 200) {
                    this.songs = data.songs;

                } else {
                    if (status_code != 422) {
                        this.message = data.message;
                    } else {
                        this.message = "Por favor, introduce un término de búsqueda"
                    }
                    
                    this.showNotification(this.message, 'error');
                }
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
                
                let status_code = response.status;
                let data = await response.json();
                let message = data.message;

                if (status_code == 204) {
                    this.showNotification(message, 'info');
                }

                else {
                    
                    this.showNotification(message, 'error');
                }


            } catch (e) {
                console.log(e);
            }

        }
    }
}

</script>

<style>

</style>