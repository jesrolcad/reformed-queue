<template>

    <div>
        <h1> Página de Token</h1>
        <p> Código de acceso obtenido correctamente</p>
        <!-- Create a button -->
        <button class="button is-primary" @click="redirectToSearcher">Buscar canciones</button>
    </div>

</template>

<script>

export default {
    data() {
        return {
            code: this.$route.query.code,
        }
    },

    created() {
        this.getAccessToken();
    },

    methods: {
        async getAccessToken() {
            try {

                let response = await fetch('http://localhost:8000/access-token?code=' + this.code, {
                    headers: { 'Content-Type': 'application/json'},
                    method: 'GET'
                });
                
                let data = await response.json();
                if (data.access_token) {
                    localStorage.setItem('access-token', data.access_token);
                }
                

            } catch (e) {
                console.log(e);
            }
            
        },

        redirectToSearcher() {
            this.$router.push({ name: 'SongSearcher' });
        }
    }
}



</script>

<style>

</style>