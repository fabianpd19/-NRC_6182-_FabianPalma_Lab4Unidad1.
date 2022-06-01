'''
Importanción de cada uno de las librerías a usar dentro del programa
'''

import datetime
import requests
import os
import argparse
import re
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase


class FeriadoEcuador(HolidayBase):
    """
    Clase para determinar los feriados dentro de Ecuador
    Determina si una fecha en específico es de vacaciones, de una forma rápida y directa
    por ejemplo, en el siguiente enlace tenemos fechas de días festivos en Ecuador:
    https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    
    Los atributos se heredan de la clase HolidayBase
    """     
    # ISO 3166-2 código para las principales subdiviciones, llamadas provincias
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    # TODO agrega más provincias
    PROVINCES = ["EC-P"]  

    def __init__(self, **kwargs):
        """
        Construcción de cada uno de los atributos para la clase de FeriadoEcuador
        ----
        Atributos:
        prov: str (cadena string)
            Código de provincia según ISO3166-2
        Métodos:
        __init__(self, placa, fecha, tiempo, online=False):
        Construye todos los atributos para el objeto de FeriadoEcuador
        """         
        self.pais = "ECU"
        self.prov = kwargs.pop("prov", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, anio):
        """
        Revisa si una fecha es feriado
        
        Parametros
        ----------
        anio : str (cadena string)
            año de una fecha
        Returns (Devuelve)
        -------
        Devuelve "True" si una fecha es día festivo
        de lo contraio devuelve el valor de "False"
        """                    
        #Días festivos 
        #Año nuevo 
        self[datetime.date(anio, JAN, 1)] = "Año Nuevo"
        
        # Navidad
        self[datetime.date(anio, DEC, 25)] = "Navidad"
        
        # Semana Santa
        self[easter(anio) + rd(weekday=FR(-1))] = "Semana Santa (Viernes Santo)"
        self[easter(anio)] = "Día de Pascuas [Easter Day]"
        
        # Carnaval
        total_lent_days = 46
        self[easter(anio) - datetime.timedelta(days=total_lent_days+2)] = "Lunes de carnaval "
        self[easter(anio) - datetime.timedelta(days=total_lent_days+1)] = "Martes de carnaval "
        
        # Labor day
        nombre = "Día Nacional del Trabajo [Labour Day]"
        # (Ley 858/Ley Reformatoria a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Si el feriado cae en sábado o martes
        # el descanso obligatorio irá al inmediato anterior viernes o lunes 
        # respectivamente
        if anio > 2015 and datetime.date(anio, MAY, 1).weekday() in (5,1):
            self[datetime.date(anio, MAY, 1) - datetime.timedelta(days=1)] = nombre
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906)) si el feriado cae en domingo
        # el descanso obligatorio irá al lunes siguiente
        elif anio > 2015 and datetime.date(anio, MAY, 1).weekday() == 6:
            self[datetime.date(anio, MAY, 1) + datetime.timedelta(days=1)] = nombre
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Feriados que sean en miércoles o jueves
        # Se cambiará al viernes de esa semana
        elif anio > 2015 and  datetime.date(anio, MAY, 1).weekday() in (2,3):
            self[datetime.date(anio, MAY, 1) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(anio, MAY, 1)] = nombre
        
        # Batalla de Pichincha, las reglas son iguales a las del día del trabajo
        nombre = "Batalla del Pichincha "
        if anio > 2015 and datetime.date(anio, MAY, 24).weekday() in (5,1):
            self[datetime.date(anio, MAY, 24).weekday() - datetime.timedelta(days=1)] = nombre
        elif anio > 2015 and datetime.date(anio, MAY, 24).weekday() == 6:
            self[datetime.date(anio, MAY, 24) + datetime.timedelta(days=1)] = nombre
        elif anio > 2015 and  datetime.date(anio, MAY, 24).weekday() in (2,3):
            self[datetime.date(anio, MAY, 24) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(anio, MAY, 24)] = nombre        
        
        # Primer grito de la independencia, las reglas son iguales a las del día del trabajo
        nombre = "Primer Grito de la Independencia"
        if anio > 2015 and datetime.date(anio, AUG, 10).weekday() in (5,1):
            self[datetime.date(anio, AUG, 10)- datetime.timedelta(days=1)] = nombre
        elif anio > 2015 and datetime.date(anio, AUG, 10).weekday() == 6:
            self[datetime.date(anio, AUG, 10) + datetime.timedelta(days=1)] = nombre
        elif anio > 2015 and  datetime.date(anio, AUG, 10).weekday() in (2,3):
            self[datetime.date(anio, AUG, 10) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(anio, AUG, 10)] = nombre       
        
        # Independencia de Guayaquil, las reglas son iguales a las del día del trabajo
        nombre = "Independencia de Guayaquil "
        if anio > 2015 and datetime.date(anio, OCT, 9).weekday() in (5,1):
            self[datetime.date(anio, OCT, 9) - datetime.timedelta(days=1)] = nombre
        elif anio > 2015 and datetime.date(anio, OCT, 9).weekday() == 6:
            self[datetime.date(anio, OCT, 9) + datetime.timedelta(days=1)] = nombre
        elif anio > 2015 and  datetime.date(anio, MAY, 1).weekday() in (2,3):
            self[datetime.date(anio, OCT, 9) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(anio, OCT, 9)] = nombre        
        
        # Día de los difuntos
        namedd = "Día de los difuntos" 
        # Independencia de Cuenca
        nameic = "Independencia de Cuenca"
        #(Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906)) 
        # Para festivos nacionales y/o locales que coincidan en días corridos, 
        #Las siguientes reglas se aplicarán:
        if (datetime.date(anio, NOV, 2).weekday() == 5 and  datetime.date(anio, NOV, 3).weekday() == 6):
            self[datetime.date(anio, NOV, 2) - datetime.timedelta(days=1)] = namedd
            self[datetime.date(anio, NOV, 3) + datetime.timedelta(days=1)] = nameic     
        elif (datetime.date(anio, NOV, 3).weekday() == 2):
            self[datetime.date(anio, NOV, 2)] = namedd
            self[datetime.date(anio, NOV, 3) - datetime.timedelta(days=2)] = nameic
        elif (datetime.date(anio, NOV, 3).weekday() == 3):
            self[datetime.date(anio, NOV, 3)] = nameic
            self[datetime.date(anio, NOV, 2) + datetime.timedelta(days=2)] = namedd
        elif (datetime.date(anio, NOV, 3).weekday() == 5):
            self[datetime.date(anio, NOV, 2)] =  namedd
            self[datetime.date(anio, NOV, 3) - datetime.timedelta(days=2)] = nameic
        elif (datetime.date(anio, NOV, 3).weekday() == 0):
            self[datetime.date(anio, NOV, 3)] = nameic
            self[datetime.date(anio, NOV, 2) + datetime.timedelta(days=2)] = namedd
        else:
            self[datetime.date(anio, NOV, 2)] = namedd
            self[datetime.date(anio, NOV, 3)] = nameic  
            
        # Fundación de Quito, solo aplicará para la provincia de Pichincha
        # Se aplican las mismas reglas que el día de trabajo
        nombre = "Fundación de Quito "        
        if self.prov in ("EC-P"):
            if anio > 2015 and datetime.date(anio, DEC, 6).weekday() in (5,1):
                self[datetime.date(anio, DEC, 6) - datetime.timedelta(days=1)] = nombre
            elif anio > 2015 and datetime.date(anio, DEC, 6).weekday() == 6:
                self[(datetime.date(anio, DEC, 6).weekday()) + datetime.timedelta(days=1)] =nombre
            elif anio > 2015 and  datetime.date(anio, DEC, 6).weekday() in (2,3):
                self[datetime.date(anio, DEC, 6) + rd(weekday=FR)] = nombre
            else:
                self[datetime.date(anio, DEC, 6)] = nombre

class PicoPlaca:
    """
    A class to represent a vehicle 
    restriction measure (Pico y Placa) 
    - ORDENANZA METROPOLITANA No. 0305
    http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
    ...
    Attributes
    ----------
    plate : str 
        The registration or patent of a vehicle is a combination of alphabetic or numeric 
        characters that identifies and individualizes the vehicle with respect to the others; 
        
        The used format is 
        XX-YYYY or XXX-YYYY, 
        where X is a capital letter and Y is a digit.
    date : str
        Date on which the vehicle intends to transit
        It is following the 
        ISO 8601 format YYYY-MM-DD: e.g., 2020-04-22.
    time : str
        time in which the vehicle intends to transit
        It is following the format 
        HH:MM: e.g., 08:35, 19:30
    online: boolean, optional
        if online == True the abstract public holidays API will be used
    Methods
    -------
    __init__(self, plate, date, time, online=False):
        Constructs all the necessary attributes 
        for the PicoPlaca object.
    plate(self):
        Gets the plate attribute value
    plate(self, value):
        Sets the plate attribute value
    date(self):
        Gets the date attribute value
    date(self, value):
        Sets the date attribute value
    time(self):
        Gets the time attribute value
    time(self, value):
        Sets the time attribute value
    __find_day(self, date):
        Returns the day from the date: e.g., Wednesday
    __is_forbidden_time(self, check_time):
        Returns True if provided time is inside the forbidden peak hours, otherwise False
    __is_holiday:
        Returns True if the checked date (in ISO 8601 format YYYY-MM-DD) is a public holiday in Ecuador, otherwise False
    predict(self):
        Returns True if the vehicle with the specified plate can be on the road at the specified date and time, otherwise False
    """ 
    #Days of the week
    __days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"]

    # Dictionary that holds the restrictions inf the form {day: forbidden last digit}
    __restrictions = {
            "Monday": [1, 2],
            "Tuesday": [3, 4],
            "Wednesday": [5, 6],
            "Thursday": [7, 8],
            "Friday": [9, 0],
            "Saturday": [],
            "Sunday": []}

    def __init__(self, placa, fecha, tiempo, online=False):
        """
        Constructs all the necessary attributes for the PicoPlaca object.
        
        Parameters
        ----------
            plate : str 
                The registration or patent of a vehicle is a combination of alphabetic or numeric 
                characters that identifies and individualizes the vehicle with respect to the others; 
                The used format is AA-YYYY or XXX-YYYY, where X is a capital letter and Y is a digit.
            date : str
                Date on which the vehicle intends to transit
                It is following the ISO 8601 format YYYY-MM-DD: e.g., 2020-04-22.
            time : str
                time in which the vehicle intends to transit
                It is following the format HH:MM: e.g., 08:35, 19:30
            online: boolean, optional
                if online == True the abstract public holidays API will be used (default is False)               
        """                
        self.placa = placa
        self.fecha = fecha
        self.tiempo = tiempo
        self.online = online


    @property
    def placa(self):
        """Gets the plate attribute value"""
        return self._plate


    @placa.setter
    def placa(self, value):
        """
        Sets the plate attribute value
        Parameters
        ----------
        value : str
        
        Raises
        ------
        ValueError
            If value string is not formated as 
            XX-YYYY or XXX-YYYY, 
            where X is a capital letter and Y is a digit
        """
        if not re.match('^[A-Z]{2,3}-[0-9]{4}$', value):
            raise ValueError(
                'The plate must be in the following format: XX-YYYY or XXX-YYYY, where X is a capital letter and Y is a digit')
        self._plate = value


    @property
    def fecha(self):
        """Gets the date attribute value"""
        return self._date


    @fecha.setter
    def fecha(self, value):
        """
        Sets the date attribute value
        Parameters
        ----------
        value : str
        
        Raises
        ------
        ValueError
            If value string is not formated as YYYY-MM-DD (e.g.: 2021-04-02)
        """
        try:
            if len(value) != 10:
                raise ValueError
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'The date must be in the following format: YYYY-MM-DD (e.g.: 2021-04-02)') from None
        self._date = value
        

    @property
    def tiempo(self):
        """Gets the time attribute value"""
        return self._time


    @tiempo.setter
    def tiempo(self, value):
        """
        Sets the time attribute value
        Parameters
        ----------
        value : str
        
        Raises
        ------
        ValueError
            If value string is not formated as HH:MM (e.g., 08:31, 14:22, 00:01)
        """
        if not re.match('^([01][0-9]|2[0-3]):([0-5][0-9]|)$', value):
            raise ValueError(
                'The time must be in the following format: HH:MM (e.g., 08:31, 14:22, 00:01)')
        self._time = value


    def __encontrarDia(self, date):
        """
        Finds the day from the date: e.g., Wednesday
        Parameters
        ----------
        date : str
            It is following the ISO 8601 format YYYY-MM-DD: e.g., 2020-04-22
        Returns
        -------
        Returns the day from the date as a string
        """        
        d = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
        return self.__days[d]


    def __tiempoProhibido(self, check_time):
        """
        Checks if the time provided is within the prohibited peak hours,
        where the peak hours are: 07:00 - 09:30 and 16:00 - 19:30
        Parameters
        ----------
        check_time : str
            Time that will be checked. It is in format HH:MM: e.g., 08:35, 19:15
        Returns
        -------
        Returns True if provided time is inside the forbidden peak hours, otherwise False
        """           
        t = datetime.datetime.strptime(check_time, '%H:%M').time()
        return ((t >= datetime.time(7, 0) and t <= datetime.time(9, 30)) or
                (t >= datetime.time(16, 0) and t <= datetime.time(19, 30)))


    def __esFeriado(self, date, online):
        """
        Checks if date (in ISO 8601 format YYYY-MM-DD) is a public holiday in Ecuador
        if online == True it will use a REST API, otherwise it will generate the holidays of the examined year
        
        Parameters
        ----------
        date : str
            It is following the ISO 8601 format YYYY-MM-DD: e.g., 2020-04-22
        online: boolean, optional
            if online == True the abstract public holidays API will be used        
        Returns
        -------
        Returns True if the checked date (in ISO 8601 format YYYY-MM-DD) is a public holiday in Ecuador, otherwise False
        """            
        y, m, d = date.split('-')

        if online:
            # abstractapi Holidays API, free version: 1000 requests per month
            # 1 request per second
            # retrieve API key from enviroment variable
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # This means there is a missing API key
                raise requests.HTTPError(
                    'Missing API key. Store your key in the enviroment variable HOLIDAYS_API_KEY')
            if response.content == b'[]':  # if there is no holiday we get an empty array
                return False
            # Fix Maundy Thursday incorrectly denoted as holiday
            if json.loads(response.text[1:-1])['name'] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_holidays = FeriadoEcuador(prov='EC-P')
            return date in ecu_holidays


    def circular(self):
        """
        Checks if vehicle with the specified plate can be on the road on the provided date and time based on the Pico y Placa rules:
        http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf    
        Returns
        -------
        Returns 
        True if the vehicle with 
        the specified plate can be on the road 
        at the specified date and time, otherwise False
        """
        # Check if date is a holiday
        if self.__esFeriado(self.fecha, self.online):
            return True

        # Check for restriction-excluded vehicles according to the second letter of the plate or if using only two letters
        # https://es.wikipedia.org/wiki/Matr%C3%ADculas_automovil%C3%ADsticas_de_Ecuador
        if self.placa[1] in 'AUZEXM' or len(self.placa.split('-')[0]) == 2:
            return True

        # Check if provided time is not in the forbidden peak hours
        if not self.__tiempoProhibido(self.tiempo):
            return True

        day = self.__encontrarDia(self.fecha)  # Find day of the week from date
        # Check if last digit of the plate is not restricted in this particular day
        if int(self.placa[-1]) not in self.__restrictions[day]:
            return True

        return False


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Pico y Placa Quito Predictor: Revisa si un auto puede cirular dependiento el día y la placa del mismo.')
    parser.add_argument(
        '-o',
        '--online',
        action='store_true',
        help='use abstract\'s Public Holidays API')
    parser.add_argument(
        '-p',
        '--plate',
        required=True,
        help='La placa de vehículo: XXX-YYYY or XX-YYYY, donde X es la letra de la capital y Y es un dígito')
    parser.add_argument(
        '-d',
        '--date',
        required=True,
        help='Fecha a comprobar: YYYY-MM-DD')
    parser.add_argument(
        '-t',
        '--time',
        required=True,
        help='Hora a comprobar: HH:MM')
    args = parser.parse_args()


    pyp = PicoPlaca(args.plate, args.date, args.time, args.online)

    if pyp.circular():
        print(
            'El vehículo con la plata {} podrá circular el {} a las {}.'.format(
                args.plate,
                args.date,
                args.time))
    else:
        print(
            'El vehículo con la plata {} no podrá circular el {} a las {}.'.format(
                args.plate,
                args.date,
                args.time))