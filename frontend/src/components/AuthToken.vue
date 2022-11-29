<template>

    <div>
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
                    window.location.href = 'http://localhost:8080/searcher';
                } // else redirect to /
                else {
                    window.location.href = 'http://localhost:8080';
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