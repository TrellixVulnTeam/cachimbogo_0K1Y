from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from servicios.serializers import *
from servicios.models import *
import random


class AsignaturaAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, format=None):
        items = Asignatura.objects.exclude(pk=19)
        serializer = AsignaturaSerializer(items, many=True)
        return Response(serializer.data)


class SubtemaTemaAPIView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, id, format=None):
        try:
            item = Subtema.objects.filter(id_tema__pk=id)
            serializer = SubtemaTemaSerializer(item, many=True)
            return Response(serializer.data)
        except Tema.DoesNotExist:
            return Response(status=404)


class TemaAsignaturaAPIView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, id, format=None):
        try:
            item = Tema.objects.filter(id_asignatura__pk=id)
            serializer = TemaAsignaturaSerializer(item, many=True)
            return Response(serializer.data)
        except Tema.DoesNotExist:
            return Response(status=404)


class TemaAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, format=None):
        items = Tema.objects.all()
        serializer = TemaSerializer(items, many=True)
        return Response(serializer.data)


class SubtemaAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, format=None):
        items = Subtema.objects.all()
        serializer = SubtemaSerializer(items, many=True)
        return Response(serializer.data)


class PreguntaAPIView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, id, format=None):
        try:
            item = Pregunta.objects.get(pk=id)
            serializer = PreguntaSerializer(item)
            return Response(serializer.data)
        except Pregunta.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Pregunta.objects.get(pk=id)
        except Pregunta.DoesNotExist:
            return Response(status=404)
        serializer = PreguntaSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Pregunta.objects.get(pk=id)
        except Pregunta.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class PreguntaTAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, id, format=None):
        items = Pregunta.objects.filter(id_subtema__id_subtema=id)
        serializer = PreguntaTSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PreguntaTSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PreguntaRAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, id, completado, format=None):
        items = Pregunta.objects.filter(id_subtema=id)
        lists = []
        response = []
        if completado == 0:
            cantidad = 7
        elif completado == 1:
            cantidad = 10
        else:
            return Response(response)
        i = 1
        while i <= cantidad:
            rand = random.choice(items).id_pregunta
            if not lists or (rand not in lists):
                lists.append(rand)
                response.append(self.get_answer(rand))
                i = i + 1

        return Response(response)

    def get_answer(self, rand):
        pregunta = Pregunta.objects.get(pk=rand)
        serializer = PreguntaTSerializer(pregunta, many=False)
        return serializer.data


class PreguntaAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, format=None):
        items = Pregunta.objects.all()
        serializer = PreguntaSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PreguntaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RespuestaAPIView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, id, format=None):
        try:
            item = Respuesta.objects.get(pk=id)
            serializer = RespuestaSerializer(item)
            return Response(serializer.data)
        except Respuesta.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Respuesta.objects.get(pk=id)
        except Respuesta.DoesNotExist:
            return Response(status=404)
        serializer = RespuestaSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Respuesta.objects.get(pk=id)
        except Respuesta.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class RespuestaPreguntaListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        items = Respuesta.objects.filter(id_pregunta__id_subtema=request.data['id_subtema'],
                                                     id_usuario=request.data['id_usuario'])
        serializer = RespuestaPreguntaSerializer(items, many=True)
        return Response(serializer.data)


class RespuestaAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, format=None):
        items = Respuesta.objects.all()
        serializer = RespuestaSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        for requests in request.data:
            try:
                Respuesta.objects.get(id_usuario=requests['id_usuario'], id_pregunta=requests['id_pregunta'])
                print(requests['id_pregunta'])
                respuesta = Respuesta.objects.get(id_usuario__pk=requests['id_usuario'],
                                                  id_pregunta__pk=requests['id_pregunta'])
                print(respuesta.id_usuario)
                respuesta.acertada = requests['acertada']
                respuesta.save(update_fields=['acertada'])
            except Respuesta.DoesNotExist:
                usuario = Usuario.objects.get(id_usuario=requests['id_usuario'])
                pregunta = Pregunta.objects.get(id_pregunta=requests['id_pregunta'])
                print(pregunta.id_pregunta)
                respuesta = Respuesta(id_usuario=usuario, id_pregunta=pregunta,
                                      acertada=requests['acertada'])
                print(respuesta)
                respuesta.save(force_insert=True)
        return Response(status=201)


class UsuarioAPIView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def put(self, request, id, format=None):
        try:
            item = Usuario.objects.get(pk=id)
        except Usuario.DoesNotExist:
            return Response(status=404)
        serializer = UsuarioSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Usuario.objects.get(pk=id)
        except Usuario.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class UsuarioAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UsuarioAuthAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        try:
            items = Usuario.objects.get(usuario=request.data['usuario'], password=request.data['password'])
            serializer = UsuarioSerializer(items)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response({"auth": False})

        return Response(status=400)


class UsuarioAsignaturaAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        items = UsuarioAsignatura.objects.filter(id_usuario_id=request.data['id_usuario'])
        serializer = UsuarioAsignaturaSerializer(items)
        return Response(serializer.data)


class UsuarioTemaAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, id, format=None):
        items = UsuarioTema.objects.filter(id_usuario=id)
        serializer = UsuarioTemaSerializer(items, many=True)
        return Response(serializer.data)


class UsuarioMonedasAPI(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        usuario = Usuario.objects.get(id_usuario=request.data['id_usuario'])
        usuario.monedas = request.data['monedas']
        usuario.save(update_fields=['monedas'])
        return Response(status=201)


class UsuarioArticuloAPI(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        usuario_articulo = UsuarioArticulo(id_usuario_id=request.data['id_usuario'],
                                           id_articulo_id=request.data['id_articulo'])
        usuario_articulo.save()
        usuario = Usuario.objects.get(id_usuario=request.data['id_usuario'])
        usuario.monedas = request.data['monedas']
        usuario.save(update_fields=['monedas'])
        return Response(status=201)


class UsuarioArticuloListAPI(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        items = UsuarioArticulo.objects.filter(id_usuario_id=request.data['id_usuario'])
        serializer = UsuarioArticuloSerializer(items, many=True)
        return Response(serializer.data)


class ArticuloAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, format=None):
        items = Articulo.objects.all()
        serializer = ArticuloSerializer(items, many=True)
        return Response(serializer.data)


class UsuarioSubtemaAPIListView(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def get(self, request, id, format=None):
        items = UsuarioSubtema.objects.filter(id_usuario=id)
        serializer = UsuarioSubtemaSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        serializer = UsuarioSubtemaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                subtema = Subtema.objects.get(pk=request.data['id_subtema'])
                u_tema = UsuarioTema.objects.get(id_tema=subtema.id_tema.id_tema, id_usuario=id)
                subtemas = Subtema.objects.filter(id_tema=subtema.id_tema.id_tema)
                id_subtemas = [id_subtema.id_subtema for id_subtema in subtemas]
                u_subtema = UsuarioSubtema.objects.filter(id_subtema__in=id_subtemas, id_usuario=id, completado=1)
                porcentaje = (u_subtema.count() / subtemas.count()) * 100
                u_tema.porcentaje = porcentaje
                u_tema.save(update_fields=['porcentaje'])
                if porcentaje == 100.00:
                    tema = Tema.objects.get(pk=u_tema.id_tema.id_tema)
                    temas = Tema.objects.filter(id_asignatura=tema.id_asignatura.id_asignatura)
                    id_temas = [id_tema.id_tema for id_tema in temas]
                    u_tema = UsuarioTema.objects.filter(id_tema__in=id_temas, id_usuario=id, porcentaje=100.00)
                    porcentaje = (u_tema.count() / temas.count()) * 100
                    u_asignatura = UsuarioAsignatura.objects.get(id_asignatura=tema.id_asignatura.id_asignatura,
                                                                 id_usuario=id)
                    u_asignatura.porcentaje = porcentaje
                    u_asignatura.save(update_fields=['porcentaje'])
                return Response(serializer.data, status=201)
            except UsuarioTema.DoesNotExist:
                porcentaje = (1 / subtemas.count()) * 100
                u_tema = UsuarioTema(id_usuario_id=id, id_temas_id=subtema.id_tema.id_tema, porcentaje=porcentaje)
                u_tema.save()
                tema = Tema.objects.get(pk=u_tema.id_tema.id_tema)
                try:
                    UsuarioAsignatura.objects.get(id_asignatura=tema.id_asignatura.id_asignatura, id_usuario_id=id)
                except Asignatura.DoesNotExist:
                    porcentaje = (1 / temas.count()) * 100
                    u_asignatura = UsuarioAsignatura(id_usuario_id=id,
                                                     id_asignatura_id=tema.id_asignatura.id_asignatura,
                                                     porcentaje=porcentaje)
                    u_asignatura.save()
                    return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
