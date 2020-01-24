// @ts-ignore
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
// @ts-ignore
import { TestBed, async } from '@angular/core/testing';

// @ts-ignore
import { Platform } from '@ionic/angular';
// @ts-ignore
import { SplashScreen } from '@ionic-native/splash-screen/ngx';
// @ts-ignore
import { StatusBar } from '@ionic-native/status-bar/ngx';

import { AppComponent } from './app.component';

// @ts-ignore
describe('AppComponent', () => {

  let statusBarSpy, splashScreenSpy, platformReadySpy, platformSpy;

  // @ts-ignore
  beforeEach(async(() => {
    // @ts-ignore
    statusBarSpy = jasmine.createSpyObj('StatusBar', ['styleDefault']);
    // @ts-ignore
    splashScreenSpy = jasmine.createSpyObj('SplashScreen', ['hide']);
    platformReadySpy = Promise.resolve();
    // @ts-ignore
    platformSpy = jasmine.createSpyObj('Platform', { ready: platformReadySpy });

    TestBed.configureTestingModule({
      declarations: [AppComponent],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
      providers: [
        { provide: StatusBar, useValue: statusBarSpy },
        { provide: SplashScreen, useValue: splashScreenSpy },
        { provide: Platform, useValue: platformSpy },
      ],
    }).compileComponents();
  }));

  // @ts-ignore
  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    // @ts-ignore
    expect(app).toBeTruthy();
  });

  // @ts-ignore
  it('should initialize the app', async () => {
    TestBed.createComponent(AppComponent);
    // @ts-ignore
    expect(platformSpy.ready).toHaveBeenCalled();
    await platformReadySpy;
    // @ts-ignore
    expect(statusBarSpy.styleDefault).toHaveBeenCalled();
    // @ts-ignore
    expect(splashScreenSpy.hide).toHaveBeenCalled();
  });

  // TODO: add more tests!

});
