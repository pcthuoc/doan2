from django.shortcuts import redirect

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print(request.user.is_authenticated)
        
        # Kiểm tra nếu người dùng chưa đăng nhập, không truy cập trang đăng nhập, không truy cập trang admin và không phải đường dẫn cần bỏ qua
        if (not request.user.is_authenticated and
            request.path != '/login/' and
            request.path != '/admin/' and
            not request.path.startswith('/update_multi/') and
            not request.path.startswith('/update/')and
            not request.path.startswith('/get/')):
            return redirect('login')
        
        return response
