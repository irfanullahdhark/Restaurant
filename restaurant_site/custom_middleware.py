from django.http import HttpResponseRedirect


class RestrictUserMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated and not request.user.is_superuser:

            restricted_urls = [
                '/admin/', '/orders/', '/undeliverable-orders/', '/orders/order_details/<int:id>/',
                '/today-deliveries/', '/users/','/users/user_details/<int:id>/','/products/',
                '/products/product_details/<int:id>/','/products/product_details/edit_product/<int:id>/',
                '/products/add_product/','/blog_posts/','/blog_posts/add_post/','/blog_posts/add_post/add_post_res/',
                '/blog_posts/add_post/post/','/blog_post/post_detail/<int:id>/','/blog_posts/delete-post/<int:id>/',
                '/gallery/','/gallery/<int:id>/','/admin/about/','/admin/about/<int:id>/','/reports/'


            ]

            if request.path in restricted_urls:
                return HttpResponseRedirect('/404/')

        if not request.user.is_authenticated:
            restricted_urls = [
                '/admin/', '/orders/', '/undeliverable-orders/', '/orders/order_details/<int:id>/',
                '/today-deliveries/', '/users/', '/users/user_details/<int:id>/', '/products/',
                '/products/product_details/<int:id>/', '/products/product_details/edit_product/<int:id>/',
                '/products/add_product/', '/blog_posts/', '/blog_posts/add_post/', '/blog_posts/add_post/add_post_res/',
                '/blog_posts/add_post/post/', '/blog_post/post_detail/<int:id>/', '/blog_posts/delete-post/<int:id>/',
                '/gallery/', '/gallery/<int:id>/', '/admin/about/', '/admin/about/<int:id>/','/reports/'
            ]
            if request.path in restricted_urls:
                return HttpResponseRedirect('/404/')

        response = self.get_response(request)
        return response


