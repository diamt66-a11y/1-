// ==========================================================================
// 구글 애드센스 승인 최적화 블로그 - 인터랙션 스크립트 (app.js)
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  // 1. 다크 모드 / 라이트 모드 테마 스위치
  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  
  // 로컬 스토리지에 테마 세팅이 저장되어 있는지 확인
  const currentTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', currentTheme);
  
  // 초기 아이콘 세팅
  if (currentTheme === 'dark') {
    themeIcon.textContent = '☀️';
  } else {
    themeIcon.textContent = '🌙';
  }

  themeToggle.addEventListener('click', () => {
    let theme = document.documentElement.getAttribute('data-theme');
    if (theme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('theme', 'light');
      themeIcon.textContent = '🌙';
    } else {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
      themeIcon.textContent = '☀️';
    }
  });

  // 2. 모바일 메뉴 반응형 토글
  const menuToggle = document.getElementById('menu-toggle');
  const navMenu = document.getElementById('nav-menu');

  if (menuToggle && navMenu) {
    menuToggle.addEventListener('click', () => {
      if (navMenu.style.display === 'flex') {
        navMenu.style.display = 'none';
      } else {
        navMenu.style.display = 'flex';
        navMenu.style.flexDirection = 'column';
        navMenu.style.position = 'absolute';
        navMenu.style.top = '100%';
        navMenu.style.left = '0';
        navMenu.style.width = '100%';
        navMenu.style.background = 'var(--bg-secondary)';
        navMenu.style.borderBottom = '1px solid var(--border-color)';
        navMenu.style.padding = '1rem';
        navMenu.style.gap = '1rem';
      }
    });

    // 화면 크기가 커지면 스타일 리셋
    window.addEventListener('resize', () => {
      if (window.innerWidth > 768) {
        navMenu.removeAttribute('style');
      }
    });
  }

  // 3. 문의 페이지 폼 전송 이벤트 시뮬레이터
  const contactForm = document.getElementById('contact-form');
  const successMessage = document.getElementById('form-success-message');

  if (contactForm && successMessage) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault(); // 실제 새로고침(전송) 차단
      
      const submitBtn = document.getElementById('submit-btn');
      submitBtn.textContent = '전송 중...';
      submitBtn.disabled = true;
 
      // 실제 네트워크 요청을 시뮬레이트하는 1초 딜레이
      setTimeout(() => {
        contactForm.style.display = 'none';
        successMessage.style.display = 'block';
      }, 1000);
    });
  }

  // 4. 동적 블로그 포스트 로드 및 렌더링 기능 추가
  const postsGrid = document.querySelector('.posts-grid');
  
  if (postsGrid) {
    fetch('posts.json')
      .then(response => {
        if (!response.ok) {
          throw new Error('포스트 데이터를 불러오는 데 실패했습니다.');
        }
        return response.json();
      })
      .then(posts => {
        renderPosts(posts);
      })
      .catch(error => {
        console.error('Error loading posts:', error);
        postsGrid.innerHTML = `
          <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-secondary);">
            <p style="font-size: 1.2rem; margin-bottom: 1rem;">⚠️ 블로그 포스트를 불러올 수 없습니다.</p>
            <small style="color: var(--accent-color);">데이터 파일을 확인해 주세요.</small>
          </div>
        `;
      });
  }

  function renderPosts(posts) {
    postsGrid.innerHTML = ''; // 기존 하드코딩된 목록 제거

    if (posts.length === 0) {
      postsGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; padding: 3rem;">아직 작성된 글이 없습니다.</p>';
      return;
    }

    posts.forEach(post => {
      const article = document.createElement('article');
      article.className = 'post-card';
      
      // 그라디언트 기본 스타일 지정
      const bgStyle = post.themeColor ? `background-image: ${post.themeColor};` : 'background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%);';

      article.innerHTML = `
        <div class="post-card-img" style="${bgStyle}"></div>
        <div class="post-card-content">
          <span class="post-category">${post.category || '일반'}</span>
          <div class="post-meta">
            <span>작성일: ${post.date}</span>
            <span>작성자: ${post.author || '솔로프레너'}</span>
          </div>
          <h2 class="post-title">
            <a href="#" class="post-link" data-id="${post.id}">${post.title}</a>
          </h2>
          <p class="post-excerpt">${post.excerpt}</p>
          <a href="#" class="read-more post-link" data-id="${post.id}">자세히 읽기 →</a>
        </div>
      `;
      postsGrid.appendChild(article);
    });

    // 글 클릭 시 팝업 혹은 동적 뷰 구현 가능 (여기서는 우선 모달/알림이나 상세 영역 스위치 준비)
    document.querySelectorAll('.post-link').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const postId = e.target.getAttribute('data-id');
        const clickedPost = posts.find(p => p.id == postId);
        if (clickedPost) {
          alert(`✏️ [${clickedPost.title}]\n\n본문 내용:\n${clickedPost.content}`);
        }
      });
    });
  }
});

