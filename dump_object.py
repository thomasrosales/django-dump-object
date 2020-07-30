from __future__ import print_function
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.core.serializers import serialize
# from future.types.newint import long
try:
    from django.db.models import loading
except ImportError:
    from django.apps import apps as loading
import json

from .utils.utils import (
    add_to_serialize_list,
    get_all_related_objects,
    serialize_me,
    seen,
    serialize_fully
)


class Command(BaseCommand):
    help = ('Dump specific objects from the database into JSON that you can '
            'use in a fixture.')
    args = '<[--kitchensink | -k] [--natural]  [--natural-primary]' \
        '[--natural-foreign]' \
        '[--attr] [--attr-val] to build the dict filter.'


    def add_arguments(self, parser):
        """Add command line arguments to parser"""

        # Required Args
        parser.add_argument(dest='model',
                            help='Name of the model, with app name first.'
                            ' Eg "app_name.model_name"')
        parser.add_argument(dest='ids',
                            default=None,
                            nargs='*',
                            help='Use a list of ids e.g. 0 1 2 3')
        parser.add_argument('--attr-filter',
                            dest='attr-filter',
                            default=None,
                            nargs='*',
                            help='Use an attribute from the model and his filter. For example: "pk__lte"')
        parser.add_argument('--attr-val',
                            dest='attr-val',
                            default=None,
                            nargs='*',
                            help='Use an value to the attr to build a filter. For example: 100')

        # Optional args
        parser.add_argument('--kitchensink', '-k',
                            action='store_true', dest='kitchensink',
                            default=False,
                            help='Attempts to get related objects as well.')
        parser.add_argument('--natural', '-n',
                            action='store_true', dest='natural',
                            default=False,
                            help='Use natural foreign and primary keys '
                            'if they are available.')
        parser.add_argument('--natural-primary',
                            action='store_true', dest='natural_primary',
                            default=False,
                            help='Use natural primary keys if they are available.')
        parser.add_argument('--natural-foreign',
                            action='store_true', dest='natural_foreign',
                            default=False,
                            help='Use natural foreign keys if they are available.')
        parser.add_argument('--no-follow',
                            action='store_false', dest='follow_fk',
                            default=True,
                            help='does not serialize Foriegn Keys related to object')
        parser.add_argument('--limit',
                            dest='limit',
                            default=250,
                            help='Use a number to limit the output result set.')
        parser.add_argument('--order-by',
                            dest='order_by',
                            default='id',
                            help='User an string attribute to order the result set.')
        parser.add_argument('--format',
                            default='json',
                            dest='format',
                            help='Specifies the output serialization format for fixtures.')

    def handle(self, *args, **options):
        error_text = ('%s\nTry calling dump_object with --help argument or ' +
                      'use the following arguments:\n %s' % self.args)
        try:
            # verify input is valid
            try:
                (app_label, model_name) = options['model'].split('.')
            except AttributeError:
                raise CommandError("Specify model as `appname.modelname")
            ids = options.get('ids', None)
            attr_filter = options.get('attr-filter')
            attr_val = options.get('attr-val')
            limit = int(options.get('limit'))
            order_by = options.get('order_by')
            if not attr_filter and not attr_val:
                raise CommandError(error_text % 'attr_filter and attr_val the both value are required.')
            if not (attr_filter or attr_val):
                raise CommandError(error_text % 'must pass list of --attr-filter and a list of --attr-val.')
            if len(attr_filter) != len(attr_val):
                raise CommandError(error_text % '--attr-filter must be equal to --attr-val.')
            if not isinstance(order_by, str):
                raise CommandError(error_text % '--order-by must be a string.')
        except IndexError:
            raise CommandError(error_text % 'No object_class or filter clause supplied.')
        except ValueError:
            raise CommandError(
                error_text %
                "object_class must be provided in the following format: app_name.model_name"
            )
        except AssertionError:
            raise CommandError(error_text % 'No filter argument supplied.')

        dump_me = loading.get_model(app_label, model_name)

        i = 0
        query = '{'
        while i < len(attr_filter):
            if i != 0:
                query += ', '
            if isinstance(attr_val[i], str):
                query += '"' + attr_filter[i] + '": "' + str(attr_val[i]) + '"'
            elif isinstance(attr_val[i], int):
                query += '"' + attr_filter[i] + '": ' + attr_val[i]
            i += 1
        query += '}'

        if query:
            result_set = dump_me.objects.filter(**json.loads(query)).order_by('-' + order_by)[:limit]
        else:
            if ids[0] == '*':
                result_set = dump_me.objects.all().order_by('-' + order_by)[:limit]
            else:
                try:
                    parsers = int, str  # long
                except NameError:
                    parsers = int, str
                for parser in parsers:
                    try:
                        result_set = dump_me.objects.filter(pk__in=map(parser, ids))
                    except ValueError:
                        pass
                    else:
                        break
                else:
                    result_set = []

        if options.get('kitchensink'):
            fields = get_all_related_objects(dump_me)

            related_fields = [rel.get_accessor_name() for rel in fields]

            for obj in result_set:
                for rel in related_fields:
                    try:
                        if hasattr(getattr(obj, rel), 'all'):
                            add_to_serialize_list(getattr(obj, rel).all())
                        else:
                            add_to_serialize_list([getattr(obj, rel)])
                    except FieldError:
                        pass
                    except ObjectDoesNotExist:
                        pass

        add_to_serialize_list(result_set)

        if options.get('follow_fk', True):
            serialize_fully()
        else:
            # reverse list to match output of serializez_fully
            serialize_me.reverse()

        natural_foreign = (options.get('natural', False) or
                           options.get('natural_foreign', False))
        natural_primary = (options.get('natural', False) or
                           options.get('natural_primary', False))

        self.stdout.write(serialize(options.get('format', 'json'),
                                    [o for o in serialize_me if o is not None],
                                    indent=4,
                                    use_natural_foreign_keys=natural_foreign,
                                    use_natural_primary_keys=natural_primary))

        # Clear the list. Useful for when calling multiple
        # dump_object commands with a single execution of django
        del serialize_me[:]
        seen.clear()
