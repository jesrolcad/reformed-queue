<template>

    <div>
        <div class="mb-3">
            <h1> Buscador de canciones</h1>
        </div>
        <!-- Create a simple searcher -->
        <div class="container text-center mb-3">
            <div class="row justify-content-start">
                <div class="col-xs-4">
                    <input v-on:keyup.enter="searchSongs" class="text-center" type="text"
                        placeholder="Canción / Artista" v-model="search">

                    <button class="border border-0 bg-transparent ms-1" @click="searchSongs">
                        <font-awesome-icon icon="fa-solid fa-magnifying-glass" class="fa-xl text-secondary"
                            title="Buscar">
                        </font-awesome-icon>
                    </button>
                </div>
            </div>
        </div>

        <div v-if="this.songs.length > 0">
            <div class="container">
                <div class="card mb-3 w-50 h-50 mx-auto" v-for="song in songs" :key="song.id">
                    <div class="row d-flex align-items-center">
                        <div class=" resize col-sm-5">
                            <img :src="song.imagen" alt="...">
                        </div>
                        <div class="col-4 md-auto d-flex mt-3">
                            <div class="card-body">
                            <h5 class="mb-0">{{ song.titulo }}</h5>
                            <p>{{ song.artista }}</p>
                        </div>
                        </div>
                        <div class="col">
                            <font-awesome-icon icon="fa-solid fa-plus" class="fa-xl" @click="addToQueue(song.id)" title="Añadir a la cola">Añadir a
                                cola</font-awesome-icon>
                        </div>
                    </div>
                </div>
            </div>
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