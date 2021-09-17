import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {

  constructor(private router: Router) {}

  slides = [
    {
      img: 'assets/img/icon.png',
      title: 'Bienvenidos a </br> SOLME VISION </br>',
      description: 'Una gran experiencia en el desarrollo de tus proyectos'
    },
    {
      img: 'assets/img/icon.png',
      title: 'Conoce nuestra APP',
      description: 'Ingresa o registrate en nuestra aplicación mediente el boton "INICIAR APLICACIÓN"'
    },
    {
      img: 'assets/img/icon.png',
      title: 'Disfruta',
      description: 'Los siguientes slides te daran una idea de como usar la aplicación'
    },
  ]

  goLogin(){
    this.router.navigate(['/login'])
  }

}
