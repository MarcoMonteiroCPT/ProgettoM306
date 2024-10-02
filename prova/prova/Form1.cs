using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace prova
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            MessageBox.Show(Cursor.Position.X + "    " + Cursor.Position.Y);
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            //MessageBox.Show(Cursor.Position.X + "    " + Cursor.Position.Y);
        }

        private void button1_Click_1(object sender, EventArgs e)
        {
            this.Cursor = createCursor((Bitmap)(sender as Button).Image);
        }

        private Cursor createCursor(Bitmap bm)
        {
            bm.MakeTransparent();
            return new Cursor(bm.GetHicon());
        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.Cursor = createCursor((Bitmap)(sender as Button).Image);
        }
    }
}
