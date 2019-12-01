var app = new Vue({
    delimiters: ['[[', ']]'],
    el:'#app',
    data: {
        current_user: 'aman',
        role: 'admin',
        menuitem: 'dashboard',
        product: 'compass',
        image: '/static/accounts/img/ams.png',
    }
})