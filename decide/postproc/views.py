from rest_framework.views import APIView
from rest_framework.response import Response

class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def paridad(self, options):
    # Calcula la suma total de votos
        total_votes = sum(opt['votes'] for opt in options)

        out = []

        for opt in options:
            # Calcula el porcentaje de votos para la opción actual
            percentage = opt['votes'] / total_votes if total_votes > 0 else 0

            # Aplica paridad ajustando los votos proporcionales
            paridad_value = int(percentage * total_votes)

            out.append({
                **opt,
                'postproc': paridad_value,
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def post(self, request):
        """
        * type: IDENTITY | PARIDAD 
        * options: [
            {
            option: str,
            number: int,
            votes: int,
            ...extraparams
            }
        ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'PARIDAD':
            return self.paridad(opts)
        # Puedes agregar más lógica para otros tipos de postprocesamiento si es necesario

        return Response({})
