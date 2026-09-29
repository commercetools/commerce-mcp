import pluralize from 'pluralize';
import {Actions, Configuration} from '../types/configuration';

type Action = {[key: string]: Permission};
type Permission = {[actions: string]: boolean};

const adminScope = ['manage_project', 'manage_api_clients', 'view_api_clients'];

// Resources without a scope of their own, keyed by the (normalized) scope
// resource that covers them — e.g. carts are governed by the order scopes
// (`view_orders`, `manage_orders`, `manage_my_orders`).
const coveredResources: {[scopeResource: string]: string[]} = {
  orders: ['cart'],
};

function normalize(str: string): string {
  return pluralize.plural(str).toLowerCase();
}

export function scopesToActions(
  scopes: Array<string>,
  configuration: Configuration
): Actions {
  const actions: Action = configuration.actions || {};
  if (scopes.some((scope) => adminScope.includes(scope))) {
    return Object.fromEntries(
      Object.entries(actions).map(
        ([resource, {read, create, update, replicate, apply}]) => {
          return [
            resource,
            {
              ...(read == undefined ? {} : {read}),
              ...(create == undefined ? {} : {create}),
              ...(update == undefined ? {} : {update}),
              ...(replicate == undefined ? {} : {replicate}),
              ...(apply == undefined ? {} : {apply}),
            },
          ];
        }
      )
    );
  }

  return scopes.reduce((acc: Action, scope: string) => {
    // eslint-disable-next-line prefer-const
    let [type, ...resourceParts] = scope.split('_');

    // for scopes such as 'manage_my_orders' => ['manage', 'my', 'orders']
    if (resourceParts[0] == 'my') {
      type = type + '_' + resourceParts.shift(); // manage_my
    }

    const resource = resourceParts.join('-');
    const normalizedResource = normalize(resource);

    const permissions =
      // eslint-disable-next-line no-nested-ternary
      type == 'view'
        ? ['read']
        : ['manage', 'manage_my'].includes(type)
          ? ['read', 'create', 'update', 'replicate', 'apply']
          : [];

    const resourceKey = Object.keys(actions).find((key) => {
      return normalizedResource.startsWith(normalize(key));
    });

    const resourceKeys = [
      ...(resourceKey ? [resourceKey] : []),
      ...(coveredResources[normalizedResource] ?? []).filter(
        (key) => key in actions
      ),
    ];

    resourceKeys.forEach((key) => {
      acc[key] = acc[key] || {};
      permissions.forEach((permission) => {
        if (permission in actions[key]) {
          acc[key][permission] = actions[key][permission];
        }
      });
    });

    return acc;
  }, {});
}
