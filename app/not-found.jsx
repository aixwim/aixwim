import { basePath } from '../lib/site';
import { CSS } from '../lib/css';

export default function NotFound() {
  return (
    <section className="nf fade">
      <style dangerouslySetInnerHTML={{ __html: CSS }} />
      <h1>404</h1>
      <p>Halaman yang Anda cari tidak ditemukan.</p>
      <a className="cat-pill" href={`${basePath}/`} style={{ display: 'inline-block' }}>← Kembali ke Beranda</a>
    </section>
  );
}
